from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Dữ liệu mô phỏng (có thể thay bằng dữ liệu thật sau)
docs = [
    Document(page_content="Chí Phèo là tác phẩm nổi tiếng của Nam Cao, phản ánh số phận người nông dân bị tha hóa."),
    Document(page_content="Nguyễn Du là đại thi hào dân tộc, tác giả của kiệt tác Truyện Kiều."),
    Document(page_content="Tác phẩm Lão Hạc thể hiện nỗi đau của người cha nghèo, viết bởi Nam Cao."),
]

# Tạo embedding & vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)

# Lưu vectorstore vào thư mục
db.save_local("vectorstore")
