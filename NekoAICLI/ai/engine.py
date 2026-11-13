import math
import random
import os
import pickle
import re

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    TfidfVectorizer = None


MODEL_PATH = "ai/model.pkl"


# ==========================================
# NEURAL NETWORK
# ==========================================

class NeuralNetwork:

    def __init__(
        self,
        input_size,
        hidden_size,
        output_size,
        learning_rate=0.1
    ):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate

        # Input → Hidden
        self.weights_input_hidden = [
            [
                random.uniform(-0.5, 0.5)
                for _ in range(hidden_size)
            ]
            for _ in range(input_size)
        ]

        self.bias_hidden = [
            0.0
            for _ in range(hidden_size)
        ]

        # Hidden → Output
        self.weights_hidden_output = [
            [
                random.uniform(-0.5, 0.5)
                for _ in range(output_size)
            ]
            for _ in range(hidden_size)
        ]

        self.bias_output = [
            0.0
            for _ in range(output_size)
        ]


    # ======================================
    # ACTIVATION
    # ======================================

    def relu(self, x):
        return max(0, x)


    def relu_derivative(self, x):

        if x > 0:
            return 1

        return 0


    def softmax(self, values):

        maximum = max(values)

        exp_values = [
            math.exp(x - maximum)
            for x in values
        ]

        total = sum(exp_values)

        return [
            x / total
            for x in exp_values
        ]


    # ======================================
    # FORWARD
    # ======================================

    def forward(self, inputs):

        hidden_raw = []
        hidden = []

        # Input → Hidden
        for j in range(self.hidden_size):

            total = self.bias_hidden[j]

            for i in range(self.input_size):

                total += (
                    inputs[i]
                    * self.weights_input_hidden[i][j]
                )

            hidden_raw.append(total)

            hidden.append(
                self.relu(total)
            )


        # Hidden → Output
        outputs_raw = []

        for j in range(self.output_size):

            total = self.bias_output[j]

            for i in range(self.hidden_size):

                total += (
                    hidden[i]
                    * self.weights_hidden_output[i][j]
                )

            outputs_raw.append(total)


        outputs = self.softmax(outputs_raw)

        return hidden_raw, hidden, outputs


    # ======================================
    # LOSS
    # ======================================

    def cross_entropy(self, prediction, target):

        return -sum(
            target[i]
            * math.log(
                max(prediction[i], 1e-12)
            )
            for i in range(self.output_size)
        )


    # ======================================
    # TRAINING
    # ======================================

    def train_one(self, inputs, target):

        # Forward
        hidden_raw, hidden, prediction = (
            self.forward(inputs)
        )


        # Loss
        loss = self.cross_entropy(
            prediction,
            target
        )


        # Output gradient
        output_gradient = [
            prediction[i] - target[i]
            for i in range(self.output_size)
        ]


        # Hidden gradient
        hidden_gradient = [
            0.0
            for _ in range(self.hidden_size)
        ]

        for i in range(self.hidden_size):

            total = 0.0

            for j in range(self.output_size):

                total += (
                    output_gradient[j]
                    * self.weights_hidden_output[i][j]
                )

            hidden_gradient[i] = (
                total
                * self.relu_derivative(hidden_raw[i])
            )


        # Hidden → Output
        for i in range(self.hidden_size):

            for j in range(self.output_size):

                gradient = (
                    hidden[i]
                    * output_gradient[j]
                )

                self.weights_hidden_output[i][j] -= (
                    self.learning_rate
                    * gradient
                )


        # Output bias
        for j in range(self.output_size):

            self.bias_output[j] -= (
                self.learning_rate
                * output_gradient[j]
            )


        # Input → Hidden
        for i in range(self.input_size):

            for j in range(self.hidden_size):

                gradient = (
                    inputs[i]
                    * hidden_gradient[j]
                )

                self.weights_input_hidden[i][j] -= (
                    self.learning_rate
                    * gradient
                )


        # Hidden bias
        for j in range(self.hidden_size):

            self.bias_hidden[j] -= (
                self.learning_rate
                * hidden_gradient[j]
            )


        return loss


# ==========================================
# TRAINING DATA
# ==========================================

training_data = [

    # ======================================
    # GREETING
    # ======================================

    ("привет", "greeting"),
    ("приветик", "greeting"),
    ("приветики", "greeting"),
    ("прив", "greeting"),
    ("привееет", "greeting"),
    ("привет неко", "greeting"),
    ("эй неко", "greeting"),
    ("хай", "greeting"),
    ("хайки", "greeting"),
    ("хай хай", "greeting"),
    ("хай ю хай", "greeting"),
    ("дарова", "greeting"),
    ("даров", "greeting"),
    ("здарова", "greeting"),
    ("здаров", "greeting"),
    ("здрасьте", "greeting"),
    ("здравствуй", "greeting"),
    ("здравствуйте", "greeting"),
    ("доброе утро", "greeting"),
    ("добрый день", "greeting"),
    ("добрый вечер", "greeting"),
    ("добры день", "greeting"),
    ("добры вечер", "greeting"),
    ("доброе утро неко", "greeting"),
    ("салют", "greeting"),
    ("йо", "greeting"),
    ("йоу", "greeting"),
    ("ку", "greeting"),
    ("ку ку", "greeting"),
    ("хелло", "greeting"),
    ("hello", "greeting"),
    ("hi", "greeting"),
    ("приветствую", "greeting"),
    ("рад тебя видеть", "greeting"),
    ("как дела", "greeting"),
    ("как ты", "greeting"),
    ("как жизнь", "greeting"),
    ("что нового", "greeting"),
    ("ну привет", "greeting"),
    ("снова привет", "greeting"),
    ("привет еще раз", "greeting"),
    ("вечер в хату", "greeting"),
    ("добрый", "greeting"),
    ("доброе", "greeting"),
    ("здорово", "greeting"),
    ("здарова неко", "greeting"),
    ("дарова неко", "greeting"),
    ("прив неко", "greeting"),
    ("хай неко", "greeting"),
    ("йо неко", "greeting"),
    ("приветик неко", "greeting"),


    # ======================================
    # TIME
    # ======================================

    ("который час", "time"),
    ("сколько времени", "time"),
    ("сколько сейчас времени", "time"),
    ("сколько время", "time"),
    ("сколько щас времени", "time"),
    ("сколько щас время", "time"),
    ("сколько сейчас время", "time"),
    ("скажи время", "time"),
    ("скажи мне время", "time"),
    ("скажи текущее время", "time"),
    ("подскажи время", "time"),
    ("подскажи мне время", "time"),
    ("покажи время", "time"),
    ("покажи текущее время", "time"),
    ("текущее время", "time"),
    ("время сейчас", "time"),
    ("которое сейчас время", "time"),
    ("можешь сказать время", "time"),
    ("можешь подсказать время", "time"),
    ("узнай время", "time"),
    ("узнай текущее время", "time"),
    ("сколько на часах", "time"),
    ("сколько сейчас на часах", "time"),
    ("что там по времени", "time"),
    ("что по времени", "time"),
    ("чо по времени", "time"),
    ("чё по времени", "time"),
    ("чо сейчас по времени", "time"),
    ("чё сейчас по времени", "time"),
    ("который щас час", "time"),
    ("который сейчас час", "time"),
    ("который час сейчас", "time"),
    ("время скажи", "time"),
    ("время покажи", "time"),
    ("скажи сколько времени", "time"),
    ("можешь сказать сколько времени", "time"),
    ("хочу узнать время", "time"),
    ("хочу знать время", "time"),
    ("надо узнать время", "time"),
    ("узнать время", "time"),
    ("пора узнать время", "time"),
    ("сколько времечко", "time"),
    ("сколько времечка", "time"),
    ("сколько время?", "time"),
    ("сколько сейчас?", "time"),
    ("который час?", "time"),
    ("чо по времени?", "time"),
    ("чё по времени?", "time"),
    ("какое время", "time"),
    ("чо по времени", "time"),
    ("чё по времени", "time"),
    ("что по времени", "time"),
    ("скажи время", "time"),
    ("какое время", "time"),
    ("который час", "time"),


    # ======================================
    # CALCULATOR
    # ======================================

    ("посчитай", "calculator"),
    ("посчитай это", "calculator"),
    ("посчитай пример", "calculator"),
    ("реши пример", "calculator"),
    ("реши это", "calculator"),
    ("сколько будет", "calculator"),
    ("вычисли", "calculator"),
    ("вычисли это", "calculator"),
    ("сосчитай", "calculator"),
    ("сосчитай это", "calculator"),

    ("сложи числа", "calculator"),
    ("сложи два числа", "calculator"),
    ("прибавь числа", "calculator"),
    ("вычти числа", "calculator"),
    ("умножь числа", "calculator"),
    ("раздели числа", "calculator"),

    ("сколько будет 2 плюс 2", "calculator"),
    ("сколько будет 5 умножить на 3", "calculator"),
    ("посчитай 10 плюс 20", "calculator"),
    ("посчитай 10 минус 3", "calculator"),
    ("посчитай 5 умножить на 4", "calculator"),
    ("посчитай 20 разделить на 5", "calculator"),

    ("вычти 2 из 4", "calculator"),
    ("вычти 5 из 10", "calculator"),
    ("вычти 7 из 20", "calculator"),

    ("отними 3 от 10", "calculator"),
    ("отними 8 от 15", "calculator"),

    ("прибавь 5 к 10", "calculator"),
    ("прибавь 7 к 13", "calculator"),

    ("сложи 3 и 8", "calculator"),
    ("сложи 5 с 12", "calculator"),

    ("умножь 3 на 7", "calculator"),
    ("умножь 4 на 8", "calculator"),

    ("раздели 20 на 4", "calculator"),
    ("раздели 30 на 5", "calculator"),

    ("вычти число из числа", "calculator"),
    ("отними число от числа", "calculator"),
    ("прибавь число к числу", "calculator"),
    ("сложи два числа", "calculator"),
    ("умножь число на число", "calculator"),
    ("раздели число на число", "calculator"),

    ("подели число на число", "calculator"),
    ("поделить число на число", "calculator"),
    ("разделить число на число", "calculator"),
    ("дели число на число", "calculator"),

    ("умножь число на число", "calculator"),
    ("умножить число на число", "calculator"),


    # ======================================
    # NOTES
    # ======================================

    ("запомни", "remember"),
    ("запомни это", "remember"),
    ("запомни что", "remember"),
    ("не забудь", "remember"),
    ("сохрани", "remember"),
    ("сохрани это", "remember"),
    ("сохрани заметку", "remember"),
    ("добавь заметку", "remember"),
    ("сделай заметку", "remember"),
    ("запиши", "remember"),
    ("запиши это", "remember"),
    ("я хочу это запомнить", "remember"),
    ("мне нужно это запомнить", "remember"),

    ("запомни купить хлеб", "remember"),
    ("запомни позвонить маме", "remember"),
    ("запомни протестировать neko", "remember"),
    ("не забудь сделать проект", "remember"),
    ("сохрани что нужно сделать", "remember"),


    # ======================================
    # TASKS
    # ======================================

    ("добавь задачу", "addtask"),
    ("добавь новую задачу", "addtask"),
    ("создай задачу", "addtask"),
    ("создай новую задачу", "addtask"),
    ("поставь задачу", "addtask"),
    ("поставь новую задачу", "addtask"),
    ("добавь мне задачу", "addtask"),
    ("мне нужна задача", "addtask"),
    ("добавь в задачи", "addtask"),
    ("добавь это в задачи", "addtask"),

    ("добавь задачу сделать neko", "addtask"),
    ("создай задачу протестировать neko", "addtask"),
    ("поставь задачу сделать проект", "addtask"),
    ("добавь задачу изучить python", "addtask"),


    # ======================================
    # DATE
    # ======================================

    ("какая сегодня дата", "date"),
    ("какое сегодня число", "date"),
    ("скажи дату", "date"),
    ("скажи сегодняшнюю дату", "date"),
    ("скажи сегодняшнее число", "date"),
    ("какая дата сегодня", "date"),
    ("сегодняшняя дата", "date"),
    ("сегодня какая дата", "date"),
    ("какой сегодня день", "date"),
    ("какой сегодня день недели", "date"),
    ("что сегодня за день", "date"),
    ("что за день сегодня", "date"),
    ("сегодня какой день", "date"),
    ("число сегодня", "date"),
    ("какое число сегодня", "date"),
    ("узнай дату", "date"),
    ("узнай сегодняшнюю дату", "date"),
    ("покажи дату", "date"),
    ("покажи сегодняшнюю дату", "date"),
    ("покажи число", "date"),
    ("скажи число", "date"),
    ("какой сегодня день недели", "date"),
    ("какой день недели сегодня", "date"),
    ("какой сегодня день?", "date"),
    ("что за день?", "date"),
    ("чо за день", "date"),
    ("чё за день", "date"),
    ("чо сегодня за день", "date"),
    ("чё сегодня за день", "date"),
    ("какое сегодня число?", "date"),
    ("какая сегодня дата?", "date"),
    ("какая дата?", "date"),
    ("какое число?", "date"),
    ("какой день сегодня", "date"),
    ("какой день", "date"),
    ("сегодня какой день", "date"),
    ("сегодняшнее число", "date"),
    ("сегодняшний день", "date"),
    ("сегодня дата", "date"),
    ("хочу узнать дату", "date"),
    ("хочу узнать число", "date"),
    ("хочу знать дату", "date"),
    ("надо узнать дату", "date"),
    ("узнать дату", "date"),
    ("узнать число", "date"),
    ("что сегодня", "date"),
    ("какой сегодня дент", "date"),
    ("какой сегодня ден", "date"),
    ("какоц сегодня день", "date"),
    ("чо по дате", "date"),
    ("чё по дате", "date"),
    ("что по дате", "date"),
    ("какая дата", "date"),


    # ======================================
    # NOTE GET
    # ======================================

    ("покажи мои заметки", "note_get"),
    ("покажи заметки", "note_get"),
    ("какие у меня заметки", "note_get"),
    ("какие заметки у меня есть", "note_get"),
    ("открой заметки", "note_get"),
    ("покажи список заметок", "note_get"),
    ("выведи мои заметки", "note_get"),
    ("что я записывал", "note_get"),


    # ======================================
    # NOTE DELETE
    # ======================================

    ("удали заметку", "note_del"),
    ("удали мою заметку", "note_del"),
    ("забудь заметку", "note_del"),
    ("удали заметку школа", "note_del"),
    ("забудь заметку школа", "note_del"),
    ("удали запись", "note_del"),


    # ======================================
    # TASK GET
    # ======================================

    ("покажи мои задачи", "task_get"),
    ("покажи задачи", "task_get"),
    ("какие у меня задачи", "task_get"),
    ("какие задачи у меня есть", "task_get"),
    ("открой задачи", "task_get"),
    ("покажи список задач", "task_get"),
    ("выведи мои задачи", "task_get"),
    ("что у меня по задачам", "task_get"),


    # ======================================
    # TASK COMPLETE
    # ======================================

    ("выполни задачу", "task_complete"),
    ("заверши задачу", "task_complete"),
    ("отметь задачу выполненной", "task_complete"),
    ("выполни задачу купить молоко", "task_complete"),
    ("заверши задачу купить молоко", "task_complete"),
    ("отметь задачу купить молоко выполненной", "task_complete"),


    # ======================================
    # TASK DELETE
    # ======================================

    ("удали задачу", "task_del"),
    ("удали мою задачу", "task_del"),
    ("убери задачу", "task_del"),
    ("удали задачу купить молоко", "task_del"),
    ("убери задачу купить молоко", "task_del"),


    # ======================================
    # INFO
    # ======================================

    ("расскажи о проекте", "info"),
    ("расскажи про проект", "info"),
    ("расскажи про neko", "info"),
    ("расскажи о neko", "info"),
    ("что такое neko", "info"),
    ("что такое neko ai", "info"),
    ("что за проект neko", "info"),
    ("что за neko", "info"),
    ("информация о проекте", "info"),
    ("информация про проект", "info"),
    ("дай информацию о проекте", "info"),
    ("покажи информацию о проекте", "info"),
    ("покажи информацию", "info"),
    ("расскажи что нибудь о проекте", "info"),
    ("что можешь рассказать о проекте", "info"),
    ("что можешь рассказать про neko", "info"),
    ("расскажи мне о neko", "info"),
    ("хочу узнать о проекте", "info"),
    ("хочу узнать про neko", "info"),
    ("узнать о проекте", "info"),
    ("узнать про neko", "info"),

    ("подробно расскажи о проекте", "info"),
    ("расскажи подробно о проекте", "info"),
    ("дай подробную информацию о проекте", "info"),
    ("покажи подробную информацию", "info"),
    ("полная информация о проекте", "info"),
    ("полная информация про neko", "info"),
    ("расскажи всё о проекте", "info"),
    ("расскажи все о neko", "info"),


    # ======================================
    # PROFILE
    # ======================================

    ("покажи мой профиль", "profile"),
    ("открой мой профиль", "profile"),
    ("покажи профиль", "profile"),
    ("открой профиль", "profile"),
    ("мой профиль", "profile"),
    ("профиль", "profile"),
    ("хочу посмотреть профиль", "profile"),
    ("покажи информацию обо мне", "profile"),
    ("покажи данные моего аккаунта", "profile"),
    ("открой мой аккаунт", "profile"),
    ("покажи мой аккаунт", "profile"),
    ("хочу посмотреть аккаунт", "profile"),
    ("покажи мои данные", "profile"),
    ("покажи информацию моего аккаунта", "profile"),
    ("выведи мой профиль", "profile"),
    ("можно посмотреть мой профиль", "profile"),
    ("а ну покажи мой профиль", "profile"),
    ("что у меня в профиле", "profile"),
    ("что там с моим профилем", "profile"),
    ("покажи кто я", "profile"),


    # ======================================
    # SETTINGS
    # ======================================

    ("поставь тему ocean", "settings"),
    ("смени тему на dark", "settings"),
    ("включи тему midnight", "settings"),
    ("установи тему forest", "settings"),
    ("поставь тему purple", "settings"),

    ("смени язык на русский", "settings"),
    ("смени язык на английский", "settings"),
    ("поставь русский язык", "settings"),
    ("поставь английский язык", "settings"),
    ("переключи язык на английский", "settings"),

    ("измени тему", "settings"),
    ("измени язык", "settings"),
    ("поменяй тему", "settings"),
    ("поменяй язык", "settings"),
    ("настройки", "settings"),


    # ======================================
    # CHANGELOG
    # ======================================

    ("покажи изменения", "changelog"),
    ("покажи лог", "changelog"),
    ("покажи changelog", "changelog"),
    ("покажи изменения neko", "changelog"),
    ("что нового", "changelog"),
    ("что изменилось", "changelog"),
    ("какие изменения", "changelog"),
    ("какие изменения в neko", "changelog"),
    ("что нового в neko", "changelog"),
    ("что нового в проекте", "changelog"),
    ("расскажи что изменилось", "changelog"),
    ("расскажи что нового", "changelog"),
    ("хочу посмотреть изменения", "changelog"),
    ("хочу посмотреть лог", "changelog"),
    ("покажи список изменений", "changelog"),
    ("история изменений", "changelog"),


    # ======================================
    # RECONNECT
    # ======================================

    ("переподключись", "reconnect"),
    ("переподключи соединение", "reconnect"),
    ("переподключи меня", "reconnect"),
    ("переподключить", "reconnect"),
    ("подключись заново", "reconnect"),
    ("подключиться заново", "reconnect"),
    ("восстанови подключение", "reconnect"),
    ("восстанови соединение", "reconnect"),
    ("восстановить подключение", "reconnect"),
    ("восстановить соединение", "reconnect"),
    ("соединись заново", "reconnect"),
    ("соединение восстанови", "reconnect"),
    ("перезапусти соединение", "reconnect"),
    ("перезапусти подключение", "reconnect"),
    ("сделай переподключение", "reconnect"),
    ("сделай реконнект", "reconnect"),
    ("реконнект", "reconnect"),
    ("reconnect", "reconnect"),
]


# ==========================================
# TEXT DATA
# ==========================================

texts = [
    text
    for text, label in training_data
]

labels = [
    label
    for text, label in training_data
]


# ==========================================
# TF-IDF
# ==========================================

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(texts)

X = X.toarray()


# ==========================================
# CLASSES
# ==========================================

classes = [
    "greeting",
    "time",
    "date",
    "calculator",
    "remember",
    "addtask",
    "note_get",
    "note_del",
    "task_get",
    "task_complete",
    "task_del",
    "info",
    "profile",
    "settings",
    "changelog",
    "reconnect",
]


class_to_index = {
    name: index
    for index, name in enumerate(classes)
}


# ==========================================
# TARGETS
# ==========================================

targets = []

for label in labels:

    target = [
        0.0
        for _ in classes
    ]

    target[class_to_index[label]] = 1.0

    targets.append(target)


# ==========================================
# MODEL
# ==========================================

model = None


# ==========================================
# LOAD / TRAIN MODEL
# ==========================================

if os.path.exists(MODEL_PATH):

    print("[AI] Loading trained model...")

    with open(MODEL_PATH, "rb") as file:

        saved_data = pickle.load(file)

    vectorizer = saved_data["vectorizer"]
    model = saved_data["model"]
    classes = saved_data["classes"]

    print("[AI] Model loaded.")


else:

    print("[AI] Training model...")

    model = NeuralNetwork(
        input_size=len(
            vectorizer.get_feature_names_out()
        ),
        hidden_size=16,
        output_size=len(classes),
        learning_rate=0.1
    )

    for epoch in range(500):

        total_loss = 0.0

        for inputs, target in zip(
            X,
            targets
        ):

            loss = model.train_one(
                inputs,
                target
            )

            total_loss += loss


        # ==================================
        # TRAINING STATUS
        # ==================================

        if (epoch + 1) % 10 == 0:

            average_loss = (
                total_loss / len(X)
            )

            print(
                f"[AI] Epoch {epoch + 1}/500 | "
                f"Loss: {average_loss:.4f}"
            )


    os.makedirs(
        os.path.dirname(MODEL_PATH),
        exist_ok=True
    )

    with open(MODEL_PATH, "wb") as file:

        pickle.dump(
            {
                "vectorizer": vectorizer,
                "model": model,
                "classes": classes
            },
            file
        )

    print("[AI] Model trained and saved.")


# ==========================================
# TRAINING VECTORS
# ==========================================

training_vectors = vectorizer.transform(
    texts
).toarray()


# ==========================================
# AI SIMILARITY CHECK
# ==========================================

def get_similarity(text):

    vector = vectorizer.transform(
        [text]
    ).toarray()[0]

    if not any(vector):

        return 0.0


    best_similarity = 0.0


    vector_length = math.sqrt(
        sum(
            value * value
            for value in vector
        )
    )


    if vector_length == 0:

        return 0.0


    for training_vector in training_vectors:

        training_length = math.sqrt(
            sum(
                value * value
                for value in training_vector
            )
        )


        if training_length == 0:

            continue


        dot_product = sum(
            vector[i] * training_vector[i]
            for i in range(len(vector))
        )


        similarity = (
            dot_product
            / (vector_length * training_length)
        )


        if similarity > best_similarity:

            best_similarity = similarity


    return best_similarity


# ==========================================
# PREDICT
# ==========================================

def predict(text):

    text = text.strip()


    if not text:

        return {
            "intent": "unknown",
            "confidence": 0.0,
            "similarity": 0.0,
            "probabilities": {
                class_name: 0.0
                for class_name in classes
            }
        }


    # ======================================
    # SIMILARITY
    # ======================================

    similarity = get_similarity(
        text
    )


    # ======================================
    # UNKNOWN CHECK
    # ======================================

    if similarity < 0.20:

        return {
            "intent": "unknown",
            "confidence": 0.0,
            "similarity": similarity,
            "probabilities": {
                class_name: 0.0
                for class_name in classes
            }
        }


    # ======================================
    # NEURAL NETWORK
    # ======================================

    vector = vectorizer.transform(
        [text]
    )


    if vector.nnz == 0:

        return {
            "intent": "unknown",
            "confidence": 0.0,
            "similarity": similarity,
            "probabilities": {
                class_name: 0.0
                for class_name in classes
            }
        }


    vector = vector.toarray()[0]


    _, _, probabilities = model.forward(
        vector
    )


    index = probabilities.index(
        max(probabilities)
    )


    intent = classes[index]

    confidence = probabilities[index]


    return {
        "intent": intent,
        "confidence": confidence,
        "similarity": similarity,
        "probabilities": {
            classes[i]: probabilities[i]
            for i in range(len(classes))
        }
    }


# ==========================================
# CALCULATOR PARSER
# ==========================================

def parse_calculator(text):

    text = text.lower().strip()


    # Число:
    # 10
    # -10
    # 10.5
    # -10.5

    number = r"(-?\d+(?:\.\d+)?)"


    # ======================================
    # SPECIAL PHRASES
    # ======================================

    patterns = [

        # Вычитание

        (
            rf"выч(?:ти|есть)\s+{number}\s+из\s+{number}",
            lambda a, b: f"{b} - {a}"
        ),

        (
            rf"отними\s+{number}\s+от\s+{number}",
            lambda a, b: f"{b} - {a}"
        ),


        # Сложение

        (
            rf"прибавь\s+{number}\s+к\s+{number}",
            lambda a, b: f"{b} + {a}"
        ),

        (
            rf"сложи\s+{number}\s+(?:и|с)\s+{number}",
            lambda a, b: f"{a} + {b}"
        ),


        # Умножение

        (
            rf"умножь\s+{number}\s+на\s+{number}",
            lambda a, b: f"{a} * {b}"
        ),

        (
            rf"умножить\s+{number}\s+на\s+{number}",
            lambda a, b: f"{a} * {b}"
        ),

        (
            rf"умножит\s+{number}\s+на\s+{number}",
            lambda a, b: f"{a} * {b}"
        ),

        (
            rf"умножитт\s+{number}\s+на\s+{number}",
            lambda a, b: f"{a} * {b}"
        ),


        # Деление

        (
            rf"подели\s+{number}\s+на\s+{number}",
            lambda a, b: f"{a} / {b}"
        ),

        (
            rf"раздели\s+{number}\s+на\s+{number}",
            lambda a, b: f"{a} / {b}"
        ),

        (
            rf"дели\s+{number}\s+на\s+{number}",
            lambda a, b: f"{a} / {b}"
        ),

        (
            rf"поделить\s+{number}\s+на\s+{number}",
            lambda a, b: f"{a} / {b}"
        ),

        (
            rf"разделить\s+{number}\s+на\s+{number}",
            lambda a, b: f"{a} / {b}"
        ),

        (
            rf"делить\s+{number}\s+на\s+{number}",
            lambda a, b: f"{a} / {b}"
        )
    ]


    # ======================================
    # REGEX PARSING
    # ======================================

    for pattern, operation in patterns:

        match = re.fullmatch(
            pattern,
            text
        )


        if match:

            return operation(
                match.group(1),
                match.group(2)
            )


    # ======================================
    # SIMPLE REPLACEMENTS
    # ======================================

    replacements = {

        # Addition
        "плюс": "+",

        # Subtraction
        "минус": "-",


        # Multiplication

        "умножить на": "*",
        "умножь на": "*",
        "умножит на": "*",
        "умножитт на": "*",

        "умножить": "*",
        "умножь": "*",
        "умножит": "*",
        "умножитт": "*",


        # Division

        "разделить на": "/",
        "раздели на": "/",
        "поделить на": "/",
        "подели на": "/",
        "делить на": "/",
        "дели на": "/",

        "разделить": "/",
        "раздели": "/",
        "поделить": "/",
        "подели": "/",
        "делить": "/",
        "дели": "/"
    }


    for word, symbol in replacements.items():

        text = text.replace(
            word,
            f" {symbol} "
        )


    # ======================================
    # ALLOWED CHARACTERS
    # ======================================

    allowed = "0123456789+-*/(). "


    expression = "".join(
        character
        for character in text
        if character in allowed
    )


    # Убираем лишние пробелы

    expression = " ".join(
        expression.split()
    )


    if not expression:

        return None


    return expression


# ==========================================
# MATH EXPRESSION DETECTOR
# ==========================================

def is_math_expression(text):

    text = text.strip()


    if not text:

        return False


    # Должна быть хотя бы одна цифра

    if not any(
        character.isdigit()
        for character in text
    ):

        return False


    # Разрешаем только математические символы

    allowed = "0123456789+-*/%(). "


    if any(
        character not in allowed
        for character in text
    ):

        return False


    # Должна присутствовать математическая операция

    operations = "+-*/%"


    if not any(
        operation in text
        for operation in operations
    ):

        return False


    return True


# ==========================================
# AI ACTION EXTRACTION
# ==========================================

def extract_ai_action(text, intent):

    lower = text.lower().strip()

    text = text.strip()


    # =========================================================
    # REMEMBER / ADD NOTE
    # =========================================================

    if intent == "remember":

        patterns = [

            r"^запомни\s+что\s+(.+)$",

            r"^запомни\s+(.+)$",

            r"^сохрани\s+что\s+(.+)$",

            r"^сохрани\s+(.+)$",

            r"^добавь\s+заметку\s+(.+)$",

            r"^сделай\s+заметку\s+(.+)$",

            r"^запиши\s+(.+)$"
        ]

        for pattern in patterns:

            match = re.fullmatch(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                value = match.group(1).strip()

                if not value:
                    return None

                return {
                    "intent": "remember",
                    "text": value
                }

        return None


    # =========================================================
    # ADD TASK
    # =========================================================

    if intent == "addtask":

        patterns = [

            r"^добавь\s+задачу\s+(.+)$",

            r"^добавь\s+задачу:\s*(.+)$",

            r"^поставь\s+задачу\s+(.+)$",

            r"^поставь\s+мне\s+задачу\s+(.+)$",

            r"^создай\s+задачу\s+(.+)$",

            r"^создай\s+мне\s+задачу\s+(.+)$",

            r"^создай\s+для\s+меня\s+задачу\s+(.+)$"
        ]

        for pattern in patterns:

            match = re.fullmatch(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                task = match.group(1).strip()

                if not task:
                    return None

                return {
                    "intent": "addtask",
                    "task": task
                }

        return None


    # =========================================================
    # NOTE DELETE
    # =========================================================

    if intent == "note_del":

        patterns = [

            r"^удали\s+заметку\s+(.+)$",

            r"^удали\s+мою\s+заметку\s+(.+)$",

            r"^забудь\s+заметку\s+(.+)$",

            r"^забудь\s+мою\s+заметку\s+(.+)$",

            r"^удали\s+запись\s+(.+)$"
        ]

        for pattern in patterns:

            match = re.fullmatch(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                name = match.group(1).strip()

                if not name:
                    return None

                return {
                    "intent": "note_del",
                    "name": name
                }

        return None


    # =========================================================
    # TASK COMPLETE
    # =========================================================

    if intent == "task_complete":

        patterns = [

            r"^выполни\s+задачу\s+(.+)$",

            r"^выполнить\s+задачу\s+(.+)$",

            r"^выполнил\s+задачу\s+(.+)$",

            r"^сделал\s+задачу\s+(.+)$",

            r"^заверши\s+задачу\s+(.+)$",

            r"^задача\s+(.+)\s+выполнена$",

            r"^задача\s+(.+)\s+готова$",

            r"^задача\s+(.+)\s+сделана$"
        ]

        for pattern in patterns:

            match = re.fullmatch(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                task = match.group(1).strip()

                if not task:
                    return None

                return {
                    "intent": "task_complete",
                    "task": task
                }

        return None


    # =========================================================
    # TASK DELETE
    # =========================================================

    if intent == "task_del":

        patterns = [

            r"^удали\s+задачу\s+(.+)$",

            r"^удали\s+мою\s+задачу\s+(.+)$",

            r"^убери\s+задачу\s+(.+)$",

            r"^убери\s+мою\s+задачу\s+(.+)$"
        ]

        for pattern in patterns:

            match = re.fullmatch(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                task = match.group(1).strip()

                if not task:
                    return None

                return {
                    "intent": "task_del",
                    "task": task
                }

        return None


    # =========================================================
    # SETTINGS
    # =========================================================

    if intent == "settings":

        # -----------------------------
        # THEME
        # -----------------------------

        theme_match = re.search(
            r"(?:поставь|смени|включи|установи|измени|поменяй)"
            r"\s+тему(?:\s+на)?\s+([a-zA-Zа-яА-Я0-9_-]+)",
            text,
            re.IGNORECASE
        )

        if theme_match:

            return {
                "intent": "settings",
                "setting": "theme",
                "value": theme_match.group(1).lower()
            }


        # -----------------------------
        # LANGUAGE
        # -----------------------------

        language_match = re.search(
            r"(?:смени|поставь|установи|переключи|измени|поменяй)"
            r"\s+язык(?:\s+на)?\s+(русский|английский|ru|en)",
            text,
            re.IGNORECASE
        )

        if language_match:

            value = language_match.group(1).lower()

            language_map = {
                "русский": "ru",
                "ru": "ru",
                "английский": "en",
                "en": "en"
            }

            return {
                "intent": "settings",
                "setting": "language",
                "value": language_map[value]
            }


        return None


    # =========================================================
    # INFO
    # =========================================================

    if intent == "info":

        full_words = [
            "подробно",
            "подробная",
            "подробную",
            "полная",
            "полную",
            "всё",
            "все"
        ]

        return {
            "intent": "info",
            "full": any(
                word in lower
                for word in full_words
            )
        }


    return None


# ==========================================
# AI INTENT VALIDATION
# ==========================================

def validate_ai_intent(text, intent):

    text = text.lower().strip()


    # =========================================================
    # PROFILE
    # =========================================================

    if intent == "profile":

        return True


    # =========================================================
    # GREETING
    # =========================================================

    if intent == "greeting":

        keywords = [
            "привет",
            "здравствуй",
            "здравствуйте",
            "добрый",
            "хай",
            "hello",
            "hi",
            "как дела",
            "как ты",
            "как поживаешь"
        ]

        return any(
            keyword in text
            for keyword in keywords
        )


    # =========================================================
    # TIME
    # =========================================================

    if intent == "time":

        keywords = [
            "время",
            "час",
            "сколько сейчас",
            "который сейчас"
        ]

        return any(
            keyword in text
            for keyword in keywords
        )


    # =========================================================
    # DATE
    # =========================================================

    if intent == "date":

        keywords = [
            "дата",
            "сегодня",
            "число",
            "какой сегодня день"
        ]

        return any(
            keyword in text
            for keyword in keywords
        )


    # =========================================================
    # NOTE GET
    # =========================================================

    if intent == "note_get":

        keywords = [
            "заметк",
            "сохранен",
            "сохранял",
            "сохраненное"
        ]

        return any(
            keyword in text
            for keyword in keywords
        )


    # =========================================================
    # TASK GET
    # =========================================================

    if intent == "task_get":

        keywords = [
            "задач",
            "сделать",
            "осталось"
        ]

        return any(
            keyword in text
            for keyword in keywords
        )


    # =========================================================
    # INFO
    # =========================================================

    if intent == "info":

        keywords = [
            "проект",
            "neko",
            "neko ai",
            "информаци",
            "расскажи",
            "рассказать",
            "что такое"
        ]

        return any(
            keyword in text
            for keyword in keywords
        )


    # =========================================================
    # SETTINGS
    # =========================================================

    if intent == "settings":

        action = extract_ai_action(
            text,
            intent
        )

        return action is not None


    # =========================================================
    # PARAMETERIZED INTENTS
    # =========================================================

    if intent in [
        "remember",
        "addtask",
        "note_del",
        "task_complete",
        "task_del"
    ]:

        action = extract_ai_action(
            text,
            intent
        )

        return action is not None


    # =========================================================
    # CALCULATOR
    # =========================================================

    if intent == "calculator":

        return (
            parse_calculator(text)
            is not None
        )


    # =========================================================
    # CHANGELOG
    # =========================================================

    if intent == "changelog":

        keywords = [
            "изменени",
            "изменилось",
            "нового",
            "нововвед",
            "обновлен",
            "обновление",
            "обновили",
            "добавлено",
            "добавили",
            "поменял",
            "поменялось",
            "поменялос",
            "последн",
            "истори",
            "чего нового",
            "что нового",
            "что изменилось",
            "что изменил",
            "что добавили",
            "что добавлено",
            "список изменений",
            "история изменений",
            "changelog"
        ]

        return any(
            keyword in text
            for keyword in keywords
        )


    # =========================================================
    # RECONNECT
    # =========================================================

    if intent == "reconnect":

        keywords = [
            "переподключ",
            "переподключи",
            "переподключись",
            "подключись заново",
            "подключиться заново",
            "подключи заново",
            "подключение заново",
            "восстанови подключение",
            "восстанови соединение",
            "восстановить подключение",
            "восстановить соединение",
            "повторное подключение",
            "повторно подключ",
            "заново подключ",
            "заново установи соединение",
            "соединение восстанови",
            "соединись заново",
            "соединись с сервером",
            "соединись с базой",
            "восстанови связь",
            "восстановить связь",
            "связь с базой",
            "связь с сервером",
            "соединение с базой",
            "соединение с сервером",
            "реконнект",
            "reconnect"
        ]

        return any(
            keyword in text
            for keyword in keywords
        )


    # =========================================================
    # UNKNOWN INTENT
    # =========================================================

    return False