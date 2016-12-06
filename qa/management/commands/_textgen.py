from random import randrange, shuffle

from qa.management.commands._util import chance

words = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla faucibus ut arcu
at tempor. Mauris faucibus rhoncus blandit. Maecenas vehicula convallis viverra.
Quisque facilisis mi a quam pulvinar rhoncus. Aenean vel sem molestie, tempus sem
eget, gravida leo. Donec vulputate placerat metus, eu faucibus enim venenatis in.
Etiam condimentum, velit non tincidunt lacinia, justo lectus pulvinar diam, sit amet
venenatis libero nunc vitae diam. Nam ut felis a sapien venenatis pretium. Vivamus
ullamcorper massa sed libero ullamcorper iaculis non quis purus. Aliquam auctor dignissim
orci eget sollicitudin. Curabitur urna erat, interdum quis leo eu, commodo ultricies risus.
Ut leo elit, hendrerit eget efficitur in, elementum eget risus. In all cases, the successful AI programs
were only good
at the one particular thing for which they were
specifically designed. They didn't generalize or show flexibility, and even their creators admitted they
didn't think like humans. Some AI problems, which at first were thought to be easy, yielded no progress.
Even today, no computer can understand language as well as a three-year-old or see as well as a mouse.
After many years of effort, unfulfilled promises, and no unqualified successes,
AI started to lose its luster. Scientists in the field moved on to other areas of research.
AI start-up companies failed. And funding became scarcer. Programming computers to do even the most basic
tasks of perception, language, and behavior began to seem impossible. Today, not much has changed.
As I said earlier, there are still people who believe that AI's problems can be solved with faster
computers, but most scientists think the entire endeavor was flawed. The critics have assailed every source
 of inspiration
save one. To that one we are driven for our moral theme. When we levied upon the masters of
old they gleefully dug up the parallels to our columns. Determine the type of training examples. Before
doing anything else, the user should decide what kind of
data is to be used as a training set. In the case of handwriting analysis, for example, this might be a
single handwritten character, an entire handwritten word, or an entire line of handwriting.
Gather a training set. The training set needs to be representative of the real-world use of the function.
Thus, a set of input objects is gathered and corresponding outputs are also gathered, either from human
experts or from measurements.
Determine the input feature representation of the learned function. The accuracy of the learned function
depends strongly on how the input object is represented. Typically, the input object is transformed into a
feature vector, which contains a number of features that are descriptive of the object. The number of features
should not be too large, because of the curse of dimensionality; but should contain enough information to
accurately predict the output.
Determine the structure of the learned function and corresponding learning algorithm. For example,
the engineer may choose to use support vector machines or decision trees.
Complete the design. Run the learning algorithm on the gathered training set. Some supervised
learning algorithms require the user to determine certain control parameters. These parameters may be
adjusted by optimizing performance on a subset (called a validation set) of the training set, or via
cross-validation.
Evaluate the accuracy of the learned function. After parameter adjustment and learning,
the performance of the resulting function should be measured on a test set that is separate
from the training set.
Mr. Pickwick's apartments in Goswell Street, although on a
limited scale, were not only of a very neat and comfortable description, but peculiarly
adapted for the residence of a man of his genius and observation.
His sitting-room was the first-floor front, his bedroom the second-floor front; and thus, whether
he were sitting at his desk in his parlour, or standing before the dressing- glass in his dormitory,
he had an equal opportunity of contemplating human nature in all the numerous phases it exhibits, in that not
more populous than popular thoroughfare
While these resolute and determined preparations for the conservation of the king's peace were pending,
 Mr. Pickwick and
his friends, wholly unconscious of the mighty events in progress,
had sat quietly down to dinner; and very talkative and companionable they all were.
Mr. Pickwick was in the very act of relating his adventure of the preceding night, to the great
 amusement of his followers, Mr. Tupman especially, when the door
opened, and a somewhat forbidding countenance peeped into the room. The eyes in the forbidding
countenance looked very
earnestly at Mr. Pickwick, for several seconds, and were to all appearance satisfied with their
investigation; for the body to
which the forbidding countenance belonged, slowly brought
itself into the apartment, and presented the form of an elderly individual in top-boots--not to keep
the reader any longer
in suspense, in short, the eyes were the wandering eyes of
Mr. Grummer, and the body was the body of the same gentleman.
"""

tags = [
    'ML', 'PCA', 'LDA', 'Math', 'MATH', 'statistics', 'LearningRate',
    'ReinforcementLearning', 'DeepLearning', 'GradientDescent', 'SVD',
    'SpectralDecomposition', 'LogisticRegression', 'NN', 'LinearMap',
    'LinearRegression', 'activation', 'backpropagation', 'AI', 'StrongAI',
    'Reduction', 'regularization', 'L1', 'L2', 'Ellastic', 'kNN', 'qNN',
    'probability', 'graphs', 'hiddenlayers'
]

words = words.replace('\n', ' ')
words = words.lower().split(" ")


def generate_tags():
    res = []
    for i in range(randrange(3, 7)):
        shuffle(tags)
        res.append('#' + tags[0])
    return ' '.join(res)


def generate(len_min, len_max, is_q=False):
    first = True
    text = []

    for k in range(randrange(len_min, len_max)):
        for i in range(randrange(7, 20)):
            j = randrange(0, len(words))

            try:
                word = ''.join(words[j]).lower().replace(',', '').replace('.', '').\
                    replace('\n', '').replace(':', '').replace('"', '')

                if first:
                    word = word.capitalize()
                first = False
                text.append(word)
            except AttributeError:
                pass

        if chance(50):
            text.append('.')
        elif chance(30):
            text.append('?')
        elif chance(10):
            text.append('!')
        else:
            text.append('...')
        first = True
    if is_q:
        text[len(text) - 1] = '?'

    text = ' '.join(text).replace(' .', '.').replace(' ?', '?').replace(' !', '!').replace(' ...', '...')
    return text

