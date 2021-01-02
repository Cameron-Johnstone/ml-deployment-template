from sentence_transformers import SentenceTransformer


def get_sentence_transformer():
    """The first time this method is run, it downloads the model and saves it locally,
    so that it doesn't have to next time it is called.
    """
    model = SentenceTransformer('bert-base-nli-stsb-mean-tokens')
    
    return model


if __name__ == "__main__":
    """This main method will be run from the Dockerfile, to download the model
    into the container at build time. This will minimize start-up time during deployment.
    """
    get_sentence_transformer()
