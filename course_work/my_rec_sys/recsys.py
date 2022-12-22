from collections import Counter

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# df = pd.read_csv('data/movies_df.csv')
df = pd.read_csv('course_work/data/movies_df.csv')
df['overview'] = df['overview'].fillna('')
indices = pd.Series(df.index, index=df['title'])


def check_movie_appearance(movie):
    return movie in df['title'].unique().tolist()


class RecommendationSystem:
    def __init__(self):
        self.plot_matrix = self.make_tfidf_matrix()
        self.metadata_matrix = self.make_countvec_matrix()

    def get_recs(self, movies, show_values=False):
        results_dict = {}
        for movie in movies:
            if movie:
                for matrix in [self.plot_matrix, self.metadata_matrix]:
                    results_dict = dict(Counter(results_dict) +
                                        Counter(self.count_top_10(movie, matrix)))
        results_dict = {k: v for k, v in sorted(results_dict.items(),
                                                key=lambda item: item[1], reverse=True)}
        results_dict = dict(list(results_dict.items())[:10])
        if show_values:
            return results_dict
        return list(results_dict.keys())

    def count_top_10(self, title, matrix):
        idx = indices[title]
        sim_scores = list(enumerate(matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        sim_scores = [(df['title'].iloc[i[0]], i[1]) for i in sim_scores]
        return dict(sim_scores)

    @staticmethod
    def min_max_scaler(array):
        return [(i - min(array)) / (max(array) - min(array))
                for i in array]

    @staticmethod
    def make_tfidf_matrix():
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['overview'])
        return linear_kernel(tfidf_matrix, tfidf_matrix)

    @staticmethod
    def make_countvec_matrix():
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(df['soup'])
        return cosine_similarity(count_matrix, count_matrix)


if __name__ == "__main__":
    movies = ['The Avengers', "Spectre", "Toy Story 3"]
    rec = RecommendationSystem()
    print(rec.get_recs(movies))
