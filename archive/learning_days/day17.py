from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer("all-MiniLM-L6-v2")


sentences = [
    "Machine Learning là gì?",
    "Machine Learning có nghĩa là gì?",
    "Python được sử dụng trong những lĩnh vực nào?"
]


embeddings = model.encode(sentences)


print("Shape:", embeddings.shape)
print()


similarity_1_2 = util.cos_sim(
    embeddings[0],
    embeddings[1]
).item()

similarity_1_3 = util.cos_sim(
    embeddings[0],
    embeddings[2]
).item()

similarity_2_3 = util.cos_sim(
    embeddings[1],
    embeddings[2]
).item()


print("Câu 1:", sentences[0])
print("Câu 2:", sentences[1])
print("Similarity:", similarity_1_2)

print()

print("Câu 1:", sentences[0])
print("Câu 3:", sentences[2])
print("Similarity:", similarity_1_3)

print()

print("Câu 2:", sentences[1])
print("Câu 3:", sentences[2])
print("Similarity:", similarity_2_3)