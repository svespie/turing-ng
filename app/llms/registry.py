LLM_REGISTRY = {}

def register_llm(name):
    def decorator(llm):
        LLM_REGISTRY[name] = llm
        return llm
    return decorator