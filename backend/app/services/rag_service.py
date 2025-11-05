"""
RAG Service for VulWeb AI Chat
Implements Retrieval-Augmented Generation using vector database and LLM
"""
import os
import json
from typing import List, Dict, Optional

# Optional imports - gracefully handle missing dependencies
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("Warning: ChromaDB not available. Vector search will be disabled.")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available. Embedding model will be disabled.")


class RAGService:
    """RAG service for intelligent chat with knowledge base"""
    
    def __init__(self, knowledge_base_path: str = None, collection_name: str = "vulweb_kb"):
        """Initialize RAG service
        
        Args:
            knowledge_base_path: Path to knowledge base directory
            collection_name: Name of the vector collection
        """
        if knowledge_base_path is None:
            knowledge_base_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 
                '..', 
                'knowledge_base'
            )
        
        self.knowledge_base_path = knowledge_base_path
        self.collection_name = collection_name
        self.kb_documents = []  # Fallback knowledge base
        
        # Initialize embedding model (using Chinese-optimized model)
        # Using 'paraphrase-multilingual-MiniLM-L12-v2' which supports Chinese
        # For better Chinese support, can use 'shibing624/text2vec-base-chinese' in production
        self.embedding_model = None
        self._init_embedding_model()
        
        # Initialize vector database
        self.chroma_client = None
        self.collection = None
        self._init_vector_db()
        
        # Load knowledge base
        self._load_knowledge_base()
    
    def _init_embedding_model(self):
        """Initialize embedding model"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            print("Sentence transformers not available, skipping embedding model initialization")
            return
        
        try:
            # Using a model that supports Chinese and is available internationally
            self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        except Exception as e:
            print(f"Warning: Failed to load embedding model: {e}")
            print("RAG service will work with reduced functionality")
    
    def _init_vector_db(self):
        """Initialize ChromaDB vector database"""
        if not CHROMADB_AVAILABLE:
            print("ChromaDB not available, skipping vector database initialization")
            return
        
        try:
            # Create persistent client
            persist_directory = os.path.join(
                os.path.dirname(__file__), 
                '..',
                '..',
                'chroma_db'
            )
            os.makedirs(persist_directory, exist_ok=True)
            
            self.chroma_client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "VulWeb knowledge base"}
            )
        except Exception as e:
            print(f"Warning: Failed to initialize vector database: {e}")
    
    def _load_knowledge_base(self):
        """Load knowledge base documents into vector database"""
        if not os.path.exists(self.knowledge_base_path):
            print(f"Knowledge base path not found: {self.knowledge_base_path}")
            return
        
        if self.collection is None or self.embedding_model is None:
            print("Vector database or embedding model not initialized, loading knowledge base for fallback search only")
            self._load_knowledge_base_fallback()
            return
        
        # Check if knowledge base already loaded
        if self.collection.count() > 0:
            print(f"Knowledge base already loaded ({self.collection.count()} documents)")
            return
        
        # Load all JSON files from knowledge base
        documents = []
        metadatas = []
        ids = []
        
        for filename in os.listdir(self.knowledge_base_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.knowledge_base_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        doc = json.load(f)
                        
                        # Create searchable text
                        searchable_text = f"{doc['title']}\n\n{doc['content']}"
                        
                        documents.append(searchable_text)
                        metadatas.append({
                            'title': doc['title'],
                            'category': doc['category'],
                            'tags': ','.join(doc['tags']),
                            'difficulty': doc['metadata']['difficulty']
                        })
                        ids.append(doc['id'])
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        if documents:
            try:
                # Generate embeddings
                embeddings = self.embedding_model.encode(documents).tolist()
                
                # Add to vector database
                self.collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"Loaded {len(documents)} documents into knowledge base")
            except Exception as e:
                print(f"Error adding documents to vector database: {e}")
    
    def _load_knowledge_base_fallback(self):
        """Load knowledge base for simple keyword search fallback"""
        self.kb_documents = []
        
        for filename in os.listdir(self.knowledge_base_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.knowledge_base_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        doc = json.load(f)
                        self.kb_documents.append(doc)
                except Exception as e:
                    print(f"Error loading {filename} for fallback: {e}")
        
        print(f"Loaded {len(self.kb_documents)} documents for fallback search")
    
    def retrieve_relevant_docs(self, query: str, n_results: int = 3) -> List[Dict]:
        """Retrieve relevant documents for a query
        
        Args:
            query: User query
            n_results: Number of results to return
            
        Returns:
            List of relevant documents with metadata
        """
        if self.collection is None or self.embedding_model is None:
            # Use fallback keyword search
            return self._retrieve_docs_fallback(query, n_results)
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search in vector database
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Format results
            relevant_docs = []
            if results['documents'] and len(results['documents']) > 0:
                for i, doc in enumerate(results['documents'][0]):
                    relevant_docs.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None
                    })
            
            return relevant_docs
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return self._retrieve_docs_fallback(query, n_results)
    
    def _retrieve_docs_fallback(self, query: str, n_results: int = 3) -> List[Dict]:
        """Simple keyword-based document retrieval fallback
        
        Args:
            query: User query
            n_results: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if not self.kb_documents:
            return []
        
        query_lower = query.lower()
        scored_docs = []
        
        for doc in self.kb_documents:
            score = 0
            # Simple keyword matching
            title_lower = doc['title'].lower()
            content_lower = doc['content'].lower()
            tags = [tag.lower() for tag in doc['tags']]
            
            # For Chinese text, check if query substring is in content
            if query_lower in title_lower:
                score += 10
            if query_lower in content_lower:
                score += 5
            for tag in tags:
                if query_lower in tag or tag in query_lower:
                    score += 8
            
            # Also check individual words (for mixed Chinese/English)
            for word in query_lower.split():
                if len(word) > 1:  # Skip single character words
                    if word in title_lower:
                        score += 3
                    if word in content_lower:
                        score += 1
                    if any(word in tag for tag in tags):
                        score += 2
            
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and return top n
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, doc in scored_docs[:n_results]:
            searchable_text = f"{doc['title']}\n\n{doc['content']}"
            results.append({
                'content': searchable_text,
                'metadata': {
                    'title': doc['title'],
                    'category': doc['category'],
                    'tags': ','.join(doc['tags']),
                    'difficulty': doc['metadata']['difficulty']
                },
                'score': score
            })
        
        return results
    
    def generate_response(
        self, 
        query: str, 
        context: Optional[Dict] = None,
        use_llm: bool = False,
        llm_config: Optional[Dict] = None
    ) -> str:
        """Generate response using RAG
        
        Args:
            query: User query
            context: Additional context (models, datasets, tasks)
            use_llm: Whether to use external LLM
            llm_config: LLM configuration (provider, api_key, endpoint, model)
            
        Returns:
            Generated response
        """
        # Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_docs(query, n_results=2)
        
        # Build context from retrieved documents
        kb_context = ""
        if relevant_docs:
            kb_context = "\n\n".join([
                f"参考资料 {i+1}：\n{doc['content']}"
                for i, doc in enumerate(relevant_docs)
            ])
        
        # Add system context
        system_context = ""
        if context:
            stats = []
            if 'models' in context:
                stats.append(f"当前有 {len(context['models'])} 个模型")
            if 'datasets' in context:
                stats.append(f"{len(context['datasets'])} 个数据集")
            if 'tasks' in context:
                running = sum(1 for t in context['tasks'] if t.get('status') == 'running')
                completed = sum(1 for t in context['tasks'] if t.get('status') == 'completed')
                stats.append(f"{running} 个训练任务正在运行，{completed} 个已完成")
            
            if stats:
                system_context = f"\n\n当前系统状态：{', '.join(stats)}"
        
        if use_llm and llm_config:
            # Use external LLM for generation
            return self._generate_with_llm(query, kb_context, system_context, llm_config)
        else:
            # Use rule-based generation with retrieved context
            return self._generate_with_rules(query, kb_context, system_context, relevant_docs)
    
    def _generate_with_rules(
        self, 
        query: str, 
        kb_context: str, 
        system_context: str,
        relevant_docs: List[Dict]
    ) -> str:
        """Generate response using rules and retrieved knowledge
        
        Args:
            query: User query
            kb_context: Knowledge base context
            system_context: System context
            relevant_docs: Retrieved documents
            
        Returns:
            Generated response
        """
        # If we have relevant knowledge base content, use it
        if relevant_docs and kb_context:
            response = f"根据系统知识库，我为您找到以下相关信息：\n\n{kb_context}"
            
            if system_context:
                response += f"\n{system_context}"
            
            # Add helpful notes
            response += "\n\n如需更详细的帮助，您可以：\n"
            response += "- 在\"系统设置\"中配置AI服务以获得更智能的回答\n"
            response += "- 查看相关页面进行实际操作\n"
            response += "- 点击快捷问题了解更多功能"
            
            return response
        
        # Fallback to basic responses
        query_lower = query.lower()
        
        if '你好' in query_lower or 'hello' in query_lower or '您好' in query_lower:
            return "您好！我是VulWeb AI助手。我可以帮您了解系统功能、指导操作流程、查询系统状态。请随时向我提问！"
        
        if '帮助' in query_lower or 'help' in query_lower:
            return """我可以帮您：
1. 了解如何上传和管理模型
2. 了解如何上传和管理数据集
3. 指导创建和监控训练任务
4. 查询系统状态和统计信息
5. 解答使用过程中的问题

请告诉我您需要哪方面的帮助？"""
        
        return "抱歉，我暂时无法理解您的问题。建议您：\n1. 在\"系统设置\"中配置AI服务以获得更智能的对话体验\n2. 尝试使用快捷问题\n3. 查看系统帮助文档"
    
    def _generate_with_llm(
        self, 
        query: str, 
        kb_context: str, 
        system_context: str,
        llm_config: Dict
    ) -> str:
        """Generate response using external LLM API
        
        Args:
            query: User query
            kb_context: Knowledge base context
            system_context: System context
            llm_config: LLM configuration
            
        Returns:
            Generated response from LLM
        """
        provider = llm_config.get('provider', 'qwen')
        
        # Build prompt with context
        system_prompt = """你是VulWeb代码漏洞检测模型管理系统的AI助手。
你的任务是根据提供的知识库信息和系统状态，回答用户关于系统使用的问题。
请用简洁、准确、友好的方式回答，必要时提供步骤说明。"""
        
        user_prompt = f"用户问题：{query}\n\n"
        if kb_context:
            user_prompt += f"知识库相关内容：\n{kb_context}\n\n"
        if system_context:
            user_prompt += f"{system_context}\n\n"
        user_prompt += "请根据以上信息回答用户问题。"
        
        try:
            if provider == 'qwen':
                return self._call_qwen_api(system_prompt, user_prompt, llm_config)
            elif provider == 'ernie':
                return self._call_ernie_api(system_prompt, user_prompt, llm_config)
            elif provider == 'zhipu':
                return self._call_zhipu_api(system_prompt, user_prompt, llm_config)
            elif provider == 'openai':
                return self._call_openai_api(system_prompt, user_prompt, llm_config)
            else:
                return f"不支持的LLM提供商: {provider}"
        except Exception as e:
            return f"调用LLM服务失败: {str(e)}。您可以在\"系统设置\"中检查API配置。"
    
    def _call_qwen_api(self, system_prompt: str, user_prompt: str, config: Dict) -> str:
        """Call Alibaba Qwen API"""
        import requests
        
        api_key = config.get('api_key')
        endpoint = config.get('endpoint', 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation')
        model = config.get('model', 'qwen-turbo')
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'input': {
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ]
            },
            'parameters': {
                'result_format': 'message'
            }
        }
        
        response = requests.post(endpoint, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        return result['output']['choices'][0]['message']['content']
    
    def _call_ernie_api(self, system_prompt: str, user_prompt: str, config: Dict) -> str:
        """Call Baidu ERNIE API"""
        import requests
        
        # ERNIE uses access token authentication
        api_key = config.get('api_key')
        secret_key = config.get('secret_key')
        
        # Get access token
        token_url = 'https://aip.baidubce.com/oauth/2.0/token'
        token_params = {
            'grant_type': 'client_credentials',
            'client_id': api_key,
            'client_secret': secret_key
        }
        token_response = requests.get(token_url, params=token_params, timeout=30)
        token_response.raise_for_status()
        access_token = token_response.json()['access_token']
        
        # Call ERNIE API
        endpoint = config.get('endpoint', 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions')
        url = f"{endpoint}?access_token={access_token}"
        
        data = {
            'messages': [
                {'role': 'user', 'content': f"{system_prompt}\n\n{user_prompt}"}
            ]
        }
        
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        return result['result']
    
    def _call_zhipu_api(self, system_prompt: str, user_prompt: str, config: Dict) -> str:
        """Call Zhipu AI API"""
        import requests
        
        api_key = config.get('api_key')
        endpoint = config.get('endpoint', 'https://open.bigmodel.cn/api/paas/v4/chat/completions')
        model = config.get('model', 'glm-4')
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ]
        }
        
        response = requests.post(endpoint, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        return result['choices'][0]['message']['content']
    
    def _call_openai_api(self, system_prompt: str, user_prompt: str, config: Dict) -> str:
        """Call OpenAI API (can also be used with compatible APIs)"""
        from openai import OpenAI
        
        api_key = config.get('api_key')
        endpoint = config.get('endpoint', 'https://api.openai.com/v1')
        model = config.get('model', 'gpt-3.5-turbo')
        
        client = OpenAI(
            api_key=api_key,
            base_url=endpoint
        )
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ]
        )
        
        return response.choices[0].message.content
    
    def reload_knowledge_base(self):
        """Reload knowledge base (useful after updates)"""
        if self.collection:
            # Clear existing collection
            self.chroma_client.delete_collection(self.collection_name)
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "VulWeb knowledge base"}
            )
        
        # Reload documents
        self._load_knowledge_base()
        
        return True


# Global RAG service instance
_rag_service = None


def get_rag_service() -> RAGService:
    """Get or create global RAG service instance"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
