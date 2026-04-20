"""
fomc_sentiment.py — FOMC Text Analysis Module
ECON 5200, Lab 23
"""

import re
from typing import Tuple, List

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

LM_NEGATIVE = set([
    'adverse', 'adversely', 'concern', 'concerned', 'concerns',
    'decline', 'declined', 'declining', 'decrease', 'decreased', 'deficit',
    'deteriorate', 'deteriorated', 'difficult', 'difficulty', 'downturn',
    'fail', 'failure', 'falling', 'loss', 'losses', 'negative', 'recession',
    'risk', 'risks', 'severe', 'slowdown', 'sluggish', 'stress', 'stressed',
    'threat', 'troubled', 'uncertain', 'uncertainty', 'unfavorable',
    'volatile', 'volatility', 'vulnerable', 'weak', 'weaken', 'weakness',
    'worsen', 'worsened'
])

LM_POSITIVE = set([
    'achieve', 'achieved', 'benefit', 'confidence', 'confident', 'favorable',
    'gain', 'gained', 'gains', 'growth', 'improve', 'improved', 'improvement',
    'improving', 'increase', 'increased', 'opportunity', 'optimism', 'optimistic',
    'positive', 'profit', 'progress', 'rebound', 'recover', 'recovery',
    'strength', 'strengthen', 'strong', 'stronger', 'success', 'successful'
])

LM_UNCERTAINTY = set([
    'approximate', 'assume', 'believe', 'cautious', 'could', 'depend', 'doubt',
    'estimate', 'expect', 'expected', 'forecast', 'likelihood', 'may', 'might',
    'nearly', 'perhaps', 'possible', 'possibly', 'predict', 'probable', 'probably',
    'roughly', 'seem', 'suggest', 'tentative', 'uncertain', 'uncertainty', 'unclear'
])

_stop_words = set(stopwords.words('english'))
_lemmatizer = WordNetLemmatizer()


def preprocess_fomc(text: str) -> str:
    """Clean and tokenize FOMC minutes text."""
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [re.sub(r'[^a-z]', '', t) for t in tokens]
    tokens = [t for t in tokens if t and t not in _stop_words and len(t) > 2]
    tokens = [_lemmatizer.lemmatize(t) for t in tokens]
    return ' '.join(tokens)


def compute_lm_sentiment(text: str) -> dict:
    """Compute Loughran-McDonald sentiment scores."""
    tokens = text.lower().split()
    total = len(tokens)
    if total == 0:
        return {'net_sentiment': 0, 'uncertainty': 0,
                'neg_count': 0, 'pos_count': 0, 'unc_count': 0, 'total_words': 0}
    neg_count = sum(1 for t in tokens if t in LM_NEGATIVE)
    pos_count = sum(1 for t in tokens if t in LM_POSITIVE)
    unc_count = sum(1 for t in tokens if t in LM_UNCERTAINTY)
    return {
        'net_sentiment': (pos_count - neg_count) / total,
        'uncertainty': unc_count / total,
        'neg_count': neg_count,
        'pos_count': pos_count,
        'unc_count': unc_count,
        'total_words': total
    }


def build_tfidf_matrix(
    texts: List[str],
    min_df: int = 5,
    max_df: float = 0.85,
    max_features: int = 5000
) -> Tuple:
    """Build TF-IDF matrix from preprocessed texts."""
    vectorizer = TfidfVectorizer(
        min_df=min_df,
        max_df=max_df,
        max_features=max_features,
        ngram_range=(1, 2)
    )
    sparse_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    return sparse_matrix, feature_names, vectorizer


if __name__ == '__main__':
    test_text = 'The committee noted that inflation remained elevated above target.'
    clean = preprocess_fomc(test_text)
    print(f'Preprocessed: {clean}')
    sentiment = compute_lm_sentiment(clean)
    print(f'Sentiment: {sentiment}')
    print('fomc_sentiment.py loaded successfully.')
