import sys

from flink.plan.Environment import get_environment
from flink.plan.Constants import WriteMode
from flink.functions.GroupReduceFunction import GroupReduceFunction


class Adder(GroupReduceFunction):
    def reduce(self, iterator, collector):
        count, word = iterator.next()
        count += sum([x[0] for x in iterator])
        collector.collect((count, word))


if __name__ == '__main__':
    # get the base path out of the runtime params
    base_path = sys.argv[0]

    # we have to hard code in the path to the output because of gotcha detailed in readme
    output_file = 'file://' + base_path + '/word_count/out.txt'

    # set up the environment with a single string as the environment data
    env = get_environment()
    data = env.from_elements(
        "Who's there? I think I hear them. Stand, ho! Who's there?"
    )

    # we first map each word into a (1, word) tuple, then flat map across that, and group by the key, and sum
    # aggregate on it to get (count, word) tuples, then pretty print that out to a file.
    data.flat_map(
        lambda x, c: [(1, word) for word in x.lower().split()]
    ).group_by(1).reduce_group(Adder(), combinable = True).map(
        lambda y: 'Count: %s Word: %s' % (y[0], y[1])
    ).write_text(
        output_file, write_mode = WriteMode.OVERWRITE
    )

    # execute the plan locally.
    env.execute(local = True)
