import toolz
from docopt import docopt

__DOC = """
Calculate the interest over time for a given deposit, and interest rate.
Can set the tax rate in order to calculate actual gains.

Usage:
  interest-calc [-h | --help]
  interest-calc <deposit> <interest_rate> <duration> [--p-size=<period_size>] [--tax=<tax_rate>]

Options:
  -h --help                                     Show this help message and exit.
  <deposit>                                     Initial deposit value (investment).
  <interest>                                    Interest rate on the deposit.
  <duration>                                    Duration of the deposit (default in years).
  -p <period_size> --p-size=<period_size>]      Redefine the duration size in months.
  -t <tax_rate> --tax=<tax_rate>                Set tax rate to compute actual gains.
"""


MONTHS_IN_YEAR = 12


def _compute_interest(interest, tax_prcent, period_months, deposit):
    return deposit * interest * (1.0 - tax_prcent) * \
                (float(period_months) / float(MONTHS_IN_YEAR))


def compute_incremental_gains(deposit, interest, n_iterations, tax_percent, period_size):
    compute_deposit = toolz.partial(_compute_interest, interest, tax_percent, period_size)

    results = list(toolz.accumulate(
        lambda a, _: a + compute_deposit(a),
        [deposit for _ in range(n_iterations + 1)]
    ))

    return results


def display_results(deposit, results, duration, period_size):

    def print_iteration((i, val)):
        print 'After {} months deposit value is {}; gain of {} %.'.format(
            i * period_size,
            round(val, 3),
            round((val / deposit) * 100.0, 3),
        )

    print 'Initial deposit of {} over {} periods of {} months generate the following gains:\n'.format(
        deposit,
        duration,
        period_size,
    )
    map(print_iteration, enumerate(results[1:], 1))


def main(argv):
    args = docopt(__DOC, argv=argv[1:], help=True)

    # compute investment stages
    results = compute_incremental_gains(
        float(args['<deposit>']),
        float(args['<interest_rate>']),
        int(args['<duration>']),
        float(args['--tax'] or 0),
        int(args['--p-size'] or 12),
    )

    # print results
    display_results(
        float(args['<deposit>']), results,
        int(args['<duration>']), int(args['--p-size'] or 12)
    )
