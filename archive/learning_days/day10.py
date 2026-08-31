#thư viện re dùng xử lý chuỗi.
import re
#import dataclass để tạo class lưu trữ dữ liệu nhanh.
from dataclasses import dataclass
#import Path để xử lý đường dẫn file.
from pathlib import Path


#tạo class TextUnit lưu nội dung, tên file và tên mục (section).
@dataclass
class TextUnit:
    text: str
    source_file: str
    section_title: str | None = None


#tạo class Chunk mới để lưu thông tin chi tiết của từng khối văn bản sau khi cắt.
@dataclass
class Chunk:
    #mã định danh duy nhất cho từng chunk (vd: ai_chunk0001).
    chunk_id: str
    #nội dung văn bản của chunk.
    text: str
    #tên file gốc chứa đoạn text này.
    source_file: str
    #số lượng từ trong chunk để tiện kiểm tra.
    word_count: int


#def hàm dùng để đếm số từ.
def count_words(text: str) -> int:
    #tách chuỗi thành mảng các từ rồi đếm số lượng.
    return len(text.split())


#def hàm tách chuỗi dài thành các câu lẻ dựa vào dấu câu.
def split_sentences(text: str) -> list[str]:
    #tách chuỗi bằng regex, giữ lại dấu câu (?<=[.!?]) và cắt tại khoảng trắng \s+
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    #trả về list các câu đã được làm sạch.
    return [
        #xóa khoảng trắng 2 lề.
        sentence.strip()
        #duyệt qua từng câu trong list sentences.
        for sentence in sentences
        #chỉ lấy những câu ko bị rỗng.
        if sentence.strip()
    ]


#def hàm cắt một câu quá dài thành các đoạn nhỏ theo đúng số lượng từ.
def split_by_words(
    text: str,
    chunk_size: int
) -> list[str]:
    #tách câu thành list các từ.
    words = text.split()
    
    #tạo list rỗng để chứa các phần nhỏ.
    parts = []

    #duyệt cắt mảng words thành từng cụm, bước nhảy = chunk_size.
    for i in range(0, len(words), chunk_size):
        #cắt lấy 1 đoạn từ vị trí i đến i + chunk_size.
        part_words = words[i:i + chunk_size]

        #nối các từ lại thành chuỗi và thêm vào list parts.
        parts.append(
            " ".join(part_words)
        )

    #trả về list các phần đã cắt.
    return parts


#def hàm chia một văn bản dài thành các phần nhỏ (ưu tiên chia theo câu).
def split_long_text(
    text: str,
    chunk_size: int
) -> list[str]:
    #gọi hàm tách văn bản thành list các câu.
    sentences = split_sentences(text)
    
    #tạo list rỗng chứa kết quả.
    parts = []

    #tạo list tạm chứa các câu đang gom.
    current_sentences = []
    #biến đếm số từ của phần đang gom.
    current_word_count = 0

    #duyệt qua từng câu.
    for sentence in sentences:
        #đếm số từ của câu hiện tại.
        sentence_word_count = count_words(sentence)

        #nếu bản thân câu này dài hơn mức cho phép (chunk_size).
        if sentence_word_count > chunk_size:
            #nếu đang có gom câu nào dở dang thì chốt luôn.
            if current_sentences:
                #nối các câu lại và thêm vào parts.
                parts.append(
                    " ".join(current_sentences)
                )
                
                #reset list tạm.
                current_sentences = []
                #reset biến đếm.
                current_word_count = 0

            #gọi hàm cắt gắt theo số từ để băm nhỏ câu siêu dài này.
            parts.extend(
                split_by_words(
                    sentence,
                    chunk_size
                )
            )
            
            #bỏ qua các bước dưới, sang câu tiếp theo.
            continue

        #nếu cộng thêm câu này bị lố chunk_size -> chốt phần cũ.
        if (
            current_word_count + sentence_word_count
            > chunk_size
        ):
            #nối các câu trong list tạm và thêm vào parts.
            parts.append(
                " ".join(current_sentences)
            )
            
            #khởi tạo lại list tạm chứa luôn câu hiện tại.
            current_sentences = [sentence]
            #gán lại biến đếm bằng số từ của câu hiện tại.
            current_word_count = sentence_word_count

        #nếu chưa lố -> tiếp tục gom vào list tạm.
        else:
            #thêm câu hiện tại vào list tạm.
            current_sentences.append(sentence)
            #cộng dồn số từ.
            current_word_count += sentence_word_count

    #kết thúc vòng lặp, nếu list tạm còn chữ -> chốt nốt đưa vào parts.
    if current_sentences:
        parts.append(
            " ".join(current_sentences)
        )

    #trả về list các phần văn bản đã chia.
    return parts


#def hàm gom units thành các object Chunk hoàn chỉnh, có đánh ID và đếm từ.
def chunk_text(
    units: list[TextUnit],
    chunk_size: int = 300
) -> list[Chunk]:
    #tạo list rỗng để lưu list các chuỗi (text) đã gom.
    chunk_texts = []

    #list tạm để gom các phần văn bản.
    current_parts = []
    #biến đếm tổng số từ của list tạm.
    current_word_count = 0

    #duyệt qua từng unit.
    for unit in units:
        #gọi hàm cắt unit ra thành các phần nhỏ.
        unit_parts = split_long_text(
            unit.text,
            chunk_size
        )

        #duyệt qua từng phần vừa cắt.
        for part in unit_parts:
            #đếm số từ của phần hiện tại.
            part_word_count = count_words(part)

            #nếu gom phần này vào mà lố chunk_size -> chốt list tạm.
            if (
                current_word_count + part_word_count
                > chunk_size
            ):
                #nếu list tạm đang có chữ.
                if current_parts:
                    #nối các phần lại và đưa vào chunk_texts.
                    chunk_texts.append(
                        " ".join(current_parts)
                    )

                #khởi tạo lại list tạm chứa luôn phần hiện tại.
                current_parts = [part]
                #gán lại biến đếm.
                current_word_count = part_word_count

            #nếu chưa lố -> tiếp tục gom vào list tạm.
            else:
                #thêm phần hiện tại vào list tạm.
                current_parts.append(part)
                #cộng dồn số từ.
                current_word_count += part_word_count

    #kết thúc vòng lặp, nếu list tạm còn chữ -> chốt nốt đưa vào chunk_texts.
    if current_parts:
        chunk_texts.append(
            " ".join(current_parts)
        )

    #nếu đầu vào ko có unit nào -> trả về list rỗng luôn.
    if not units:
        return []

    #lấy tên file từ unit đầu tiên (giả định các unit cùng 1 file).
    source_file = units[0].source_file
    #dùng Path để lấy mỗi tên file, bỏ đi phần đuôi mở rộng (vd: ai.md -> ai).
    file_name = Path(source_file).stem

    #tạo list rỗng để chứa các object Chunk thành phẩm.
    chunks = []

    #duyệt qua list text đã gom, dùng enumerate để tự động đếm số thứ tự từ 1.
    for i, text in enumerate(
        chunk_texts,
        start=1
    ):
        #tạo object Chunk mới.
        chunk = Chunk(
            #tạo ID format: tênfile_chunk0001 (dùng :04d để thêm số 0 ở đầu cho đủ 4 chữ số).
            chunk_id=f"{file_name}_chunk{i:04d}",
            #gán nội dung text.
            text=text,
            #gán tên file gốc.
            source_file=source_file,
            #đếm và gán tổng số từ.
            word_count=count_words(text)
        )

        #thêm object vừa tạo vào list kết quả.
        chunks.append(chunk)

    #trả về danh sách object Chunk.
    return chunks


#Code test tạo dữ liệu giả.
units = [
    #tạo unit 1
    TextUnit(
        text="Machine Learning là một nhánh của AI.",
        source_file="ai.md",
        section_title="Machine Learning"
    ),
    #tạo unit 2
    TextUnit(
        text="Machine Learning cho phép máy tính học từ dữ liệu.",
        source_file="ai.md",
        section_title="Machine Learning"
    ),
    #tạo unit 3
    TextUnit(
        text="Học có giám sát là sử dụng tập dữ liệu có nhãn.",
        source_file="ai.md",
        section_title="Deep Learning"
    )
]


#chạy hàm gom chunk với giới hạn nhỏ (20 từ) để test.
chunks = chunk_text(
    units,
    chunk_size=20
)


#duyệt qua list chunks và in kết quả.
for chunk in chunks:
    #in id
    print("ID:", chunk.chunk_id)
    #in file nguồn
    print(
        "Source:",
        chunk.source_file
    )
    #in số lượng từ
    print(
        "Words:",
        chunk.word_count
    )
    #in nội dung text
    print(
        "Text:",
        chunk.text
    )
    #in đường gạch ngang phân cách
    print("-" * 50)