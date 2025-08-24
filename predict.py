# import joblib

# # this is all to test the model to make sure it was working at first.
# def load_model():
#     model_path = "toxicity_model.pkl"
#     print(f"Loading model from: {model_path}")
#     model = joblib.load(model_path)
#     return model

# def predict(text):
#     model = load_model()
#     pred = model.predict([text])
#     return pred[0]

# if __name__ == "__main__":
#     test_comments = [
#         "This comment is hateful and toxic.",
#         "I really enjoyed the movie, it was fantastic!",
#         "You are an idiot and should shut up.",
#         "Thanks for the update, I appreciate your help."
#     ]

#     for idx, comment in enumerate(test_comments, 1):
#         prediction = predict(comment)
#         print(f"Test comment {idx}: \"{comment}\"")
#         print(f"Prediction: {'Toxic' if prediction == 1 else 'Not toxic'}\n")
