# -*- coding: utf-8 -*-
import pickle
import numpy as np
import os
from utils.load import get_similarity_scores, get_idx_to_mid, get_mid_to_idx, \
    get_movies, get_movie_name

similarity_scores = get_similarity_scores()
idx_to_mid = get_idx_to_mid()
mid_to_idx = get_mid_to_idx()
movies = get_movies()

def load_files():
    global similarity_scores
    global idx_to_mid
    global mid_to_idx
    global movies
    similarity_scores = get_similarity_scores()
    idx_to_mid = get_idx_to_mid()
    mid_to_idx = get_mid_to_idx()
    movies = get_movies()


def get_sim_scores(list_mids):
    # We get the list of idx from the list of mid
    list_idx = [mid_to_idx[int(id)] for id in list_mids]
    #list_idx = mid_to_idx[int(id)]
    sims = similarity_scores[list_idx]

    # Trick to sum similarities if user selects multiple rows
    sims = np.sum(sims, axis=0)

    return sims

def get_ranked_recos(sims):
    recos = []
    for idx in np.argsort(-sims):
        mid = idx_to_mid[idx]
        name = get_movie_name(mid, get_movies())
        #name = movies[movies['movieId']==mid]['title'].values[0]
        score = sims[idx]
        recos.append((mid, name, score))
    return recos

def get_reco(list_mids, N=5, exclude_selection=False):
    if (similarity_scores is None):
        return None

    # Retrieve recommendations
    sims = get_sim_scores(list_mids)
    recos = get_ranked_recos(sims)

    # Exclude selection from results
    if exclude_selection is True:
        recos = [r for r in recos if str(r[0]) not in list_mids]

    # Limiting to N results for display
    recos = recos[:N]
    print("Recommendations:", recos)

    return recos
