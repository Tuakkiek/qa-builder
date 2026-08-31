#import hàm extract_md và class TextUnit từ file day05.
from day05 import extract_md, TextUnit


#def hàm dùng để đếm số từ.
def count_words(text: str) -> int:
    return len(text.split())


#def hàm lấy phần text lặp lại (overlap) ở cuối chunk cũ để nối sang chunk mới.
def get_overlap_text(text: str, overlap_words: int) -> str:
    #nếu số từ cần lặp lại <= 0 thì ko lấy gì cả.
    if overlap_words <= 0:
        return ""

    words = text.split()
    
    #lấy n từ cuối cùng của chuỗi và nối lại bằng khoảng trắng.
    return " ".join(words[-overlap_words:])


#def hàm gom các đoạn văn thành các chunks lớn, có nối chồng 1 phần chữ (overlap) để giữ ngữ cảnh.
def chunk_text(
    units: list[TextUnit],
    chunk_size: int = 300,
    overlap_ratio: float = 0.15 #tỷ lệ chữ lặp lại giữa các chunk (vd: 15%).
) -> list[str]:

    chunks: list[str] = []

    current_chunk: list[str] = []
    current_word_count = 0

    #tính ra số từ cụ thể sẽ được lặp lại dựa trên giới hạn chunk và tỷ lệ.
    overlap_words = int(chunk_size * overlap_ratio)

    for unit in units:
        unit_word_count = count_words(unit.text)

        if (
            current_chunk
            and current_word_count + unit_word_count > chunk_size
        ):
            chunk_text_value = "\n\n".join(current_chunk)

            chunks.append(chunk_text_value)

            #gọi hàm trích xuất đoạn đuôi của chunk vừa chốt làm mồi cho chunk sau.
            overlap_text = get_overlap_text(
                chunk_text_value,
                overlap_words
            )

            #nếu có text overlap -> khởi tạo chunk mới bắt đầu bằng đoạn text này luôn.
            if overlap_text:
                current_chunk = [overlap_text]
                current_word_count = count_words(overlap_text)
            #nếu ko -> reset list tạm về rỗng như bình thường.
            else:
                current_chunk = []
                current_word_count = 0

        current_chunk.append(unit.text)
        current_word_count += unit_word_count

    if current_chunk:
        chunk_text_value = "\n\n".join(current_chunk)
        chunks.append(chunk_text_value)

    return chunks


#Code bên dưới chỉ chạy khi file này được gọi trực tiếp.
if __name__ == "__main__":
    units = extract_md("data/giao-trinh-ttnt.md")

    #gọi hàm chunk_text với giới hạn 300 từ và chồng lấp 15%.
    chunks = chunk_text(
        units,
        chunk_size=300,
        overlap_ratio=0.15
    )
    #in ra màn hình các chunk.
    for index, chunk in enumerate(chunks, start=1):
        print(f"===== CHUNK {index} =====")
        print(f"Word count: {count_words(chunk)}")
        print(chunk)
        print()