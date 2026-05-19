import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# ✅ Custom sentence tokenizer using regex
def simple_sent_tokenize(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]

# --------------------- Fitness Function ---------------------
def fitness_function(sentence, vectorizer, tfidf_matrix, sentence_idx):
    words = re.findall(r'\b\w+\b', sentence.lower())
    score = 0
    for word in words:
        if word in vectorizer.vocabulary_:
            idx = vectorizer.vocabulary_[word]
            score += tfidf_matrix[sentence_idx, idx]
    return score / (len(words) + 1e-6)

# --------------------- GOA Algorithm ---------------------
def run_goa_summary(text, population_size=10, num_iterations=20, summary_ratio=0.3):
    sentences = simple_sent_tokenize(text)
    num_sentences = len(sentences)
    summary_length = max(1, int(summary_ratio * num_sentences))

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)

    population = [
        random.sample(range(num_sentences), summary_length)
        for _ in range(population_size)
    ]

    for iteration in range(num_iterations):
        fitness_scores = []
        for individual in population:
            score = sum(
                fitness_function(sentences[i], vectorizer, tfidf_matrix, i)
                for i in individual
            )
            fitness_scores.append(score)

        best_index = fitness_scores.index(max(fitness_scores))
        best_individual = population[best_index]

        new_population = []
        for individual in population:
            new_individual = []
            for i in range(summary_length):
                if random.random() < 0.5:
                    new_individual.append(best_individual[i])
                else:
                    new_individual.append(random.randint(0, num_sentences - 1))
            new_population.append(new_individual)
        population = new_population

    final_scores = [
        sum(fitness_function(sentences[i], vectorizer, tfidf_matrix, i) for i in individual)
        for individual in population
    ]
    final_best = population[final_scores.index(max(final_scores))]
    final_best.sort()

    summary = ' '.join(sentences[i] for i in final_best)
    return summary
