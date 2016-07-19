filelist = ['a8_knn_lateday_', 'a8_svm_lateday_'] #, 'cb_knn_lateday_', 'cb_svm_lateday_']

for name in filelist:

    condition_negative_file = open(name + 'np.txt')

    false_positive = 0
    false_negative = 0
    true_positive = 0
    true_negative = 0

    for line in condition_negative_file:
        if line[0] == 'p':
            false_positive = float(line.split()[1])
        elif line[0] == 'n':
            true_negative = float(line.split()[1])

    condition_positive_file = open(name + 'p.txt')

    for line in condition_positive_file:
        if line[0] == 'p':
            true_positive = float(line.split()[1])
        elif line[0] == 'n':
            false_negative = float(line.split()[1])


    total_condition_positive = true_positive + false_negative
    total_condition_negative = false_positive + true_negative

    print(name)
    print('\tTotal condition negative = ' + str(total_condition_negative))
    print('\tTotal condiion positive = ' + str(total_condition_positive))
    print('\tTrue negative = ' + str(true_negative))
    print('\tFalse positive = ' + str(false_positive))
    print('\tTrue positive = ' + str(true_positive))
    print('\tfalse negative = ' + str(false_negative))

    if total_condition_positive and total_condition_negative != 0:
        total_population = total_condition_negative + total_condition_positive

        true_positive_rate = true_positive / total_condition_positive
        false_negative_rate = false_negative / total_condition_positive
        false_positive_rate = false_positive / total_condition_negative
        true_negative_rate = true_negative / total_condition_negative

        accuracy = (true_positive + true_negative) / total_population
        percision = true_positive / (true_positive + false_positive)
        recall = true_positive_rate
        F1_score = 2.0 * ((percision * recall) / (percision + recall))

        print('\tTotal population = ' + str(total_population))

        print('\tTrue negative rate = ' + str(true_negative_rate))
        print('\tFalse negative rate = ' + str(false_negative_rate))
        print('\tFalse postive rate = ' + str(false_positive_rate))
        print('\tTrue positive rate = ' + str(true_positive_rate))

        print('\t\tAccuracy = ' + str(accuracy))
        print('\t\tF1 = ' + str(F1_score))



    else:
        print('Something was zero')



