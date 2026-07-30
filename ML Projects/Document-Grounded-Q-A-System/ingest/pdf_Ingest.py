from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    CSVLoader,
    PDFMinerLoader,  # Alternative PDF loader
    UnstructuredPDFLoader  # OCR-capable loader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
import gc
import os

def load_document(path, use_ocr=False):
    """
    Load and process documents of multiple formats: PDF, TXT, DOC, DOCX, CSV
    
    Args:
        path (str): Path to the document file
        use_ocr (bool): Use OCR for scanned PDFs (slower but handles images)
        
    Returns:
        list: List of document chunks
    """
    try:
        # Get file extension
        _, file_extension = os.path.splitext(path)
        file_extension = file_extension.lower()
        
        # Select appropriate loader based on file type
        if file_extension == '.pdf':
            # Try multiple PDF loaders
            if use_ocr:
                print(f"📄 Loading PDF with OCR: {os.path.basename(path)}")
                loader = UnstructuredPDFLoader(path)
            else:
                print(f"📄 Loading PDF: {os.path.basename(path)}")
                try:
                    loader = PyPDFLoader(path)
                except Exception as e:
                    print(f"⚠️ PyPDFLoader failed, trying PDFMiner...")
                    loader = PDFMinerLoader(path)
            
        elif file_extension == '.txt':
            loader = TextLoader(path, encoding='utf-8')
            print(f"📝 Loading TXT: {os.path.basename(path)}")
            
        elif file_extension in ['.doc', '.docx']:
            loader = UnstructuredWordDocumentLoader(path)
            print(f"📋 Loading Word Document: {os.path.basename(path)}")
            
        elif file_extension == '.csv':
            loader = CSVLoader(path, encoding='utf-8')
            print(f"📊 Loading CSV: {os.path.basename(path)}")
            
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Supported formats: PDF, TXT, DOC, DOCX, CSV")
        
        # Load documents
        docs = loader.load()
        print(f"✅ Loaded {len(docs)} page(s)")
        
        # Check if documents are empty
        total_text = "".join([doc.page_content for doc in docs])
        total_chars = len(total_text.strip())
        
        if total_chars == 0:
            raise ValueError(
                "❌ No text extracted from the document. "
                "This might be a scanned PDF (image-based). "
                "Try using OCR or convert it to text format first."
            )
        
        print(f"📝 Extracted {total_chars} characters")
        
        # Configure text splitter with more lenient settings
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=400,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            keep_separator=True
        )
        
        # Split documents into chunks
        chunks = splitter.split_documents(docs)
        
        # If still no chunks, create at least one from the full text
        if len(chunks) == 0 and total_chars > 0:
            print("⚠️ No chunks created with default settings, using full text as single chunk")
            from langchain.schema import Document
            chunks = [Document(page_content=total_text[:5000], metadata={"source": path})]
        
        print(f"✅ Created {len(chunks)} chunks")
        
        # Cleanup
        del loader
        del docs
        gc.collect()
        
        return chunks
        
    except Exception as e:
        print(f"❌ Error loading document: {e}")
        raise
        
    finally:
        # Ensure garbage collection
        gc.collect()


# Alias for backward compatibility
def load_pdf(path, use_ocr=False):
    """Backward compatible function - calls load_document"""
    return load_document(path, use_ocr=use_ocr)


