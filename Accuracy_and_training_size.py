
import glob
import shutil
import audioTrainTest as aT
import pickle


classifier_location = '/home/ryan/Desktop/AnnotatedFiles/TestingResults/classifier_location/'
percentage_to_remove = [0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0]
main_directory = '/home/ryan/Desktop/AnnotatedFiles/BackupLabelFiles/fcb'
p_directory = main_directory + '/p/'
np_directory = main_directory + '/np/'
testing_directory = '/home/ryan/Desktop/AnnotatedFiles/TestingData/fcb'
p_holding_dir = '/home/ryan/Desktop/AnnotatedFiles/holding/p/'
np_holding_dir = '/home/ryan/Desktop/AnnotatedFiles/holding/np/'
testing_p_directory = testing_directory + '/p/'
testing_np_directory = testing_directory + '/np/'
p_file_list = glob.glob(p_directory + '*.wav')
np_file_list = glob.glob(np_directory + '*.wav')

num_p_files = len(p_file_list)
num_np_files = len(np_file_list)

num_train_set_list = []
num_svm_tp = []
num_svm_tn = []
num_svm_fn = []
num_svm_fp = []

num_knn_tp = []
num_knn_fp = []
num_knn_tn = []
num_knn_fn = []

for remove_per in percentage_to_remove:
    print(remove_per)
    p_remove_num = int(round(remove_per * float(num_p_files)))
    np_remove_num = int(round(remove_per * float(num_np_files)))
    num_train_set_list.append((num_np_files + num_p_files) - (p_remove_num + np_remove_num))
    # move the files out of main directory into temp holding directory
    for i in range(0, p_remove_num):
        shutil.move(p_file_list[i], p_holding_dir)
    for i in range(0, np_remove_num):
        shutil.move(np_file_list[i], np_holding_dir)

    aT.featureAndTrain([p_directory, np_directory], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, 'svm', classifier_location + 'svm')
    aT.featureAndTrain([p_directory, np_directory], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, 'knn', classifier_location + 'knn')

    # test on the testing set
    # Copy and paste cross_validations and loop through the whole testing sets and get my own counts.
    # All we need to record are the 4 types of conditions, in 4 lists with shared indexing
    knn_true_positive = 0
    svm_true_positive = 0
    knn_false_negative = 0
    svm_false_negative = 0
    knn_true_negative = 0
    svm_true_negative = 0
    knn_false_positive = 0
    svm_false_positive = 0

    for test_file in glob.glob(testing_p_directory + '*.wav'):
        # test svm
        result_svm = aT.fileClassification(test_file, classifier_location + 'svm', 'svm')
        # test knn
        result_knn = aT.fileClassification(test_file, classifier_location + 'knn', 'knn')
        # update counts
        if result_knn[2][result_knn[0]] == 'p':
            knn_true_positive += 1
        else:
            knn_false_negative += 1

        if result_svm[2][int(result_svm[0])] == 'p':
            svm_true_positive += 1
        else:
            svm_false_negative += 1

    for test_file in glob.glob(testing_np_directory + '*.wav'):
        # test svm
        result_svm = aT.fileClassification(test_file, classifier_location + 'svm', 'svm')
        # test knn
        result_knn = aT.fileClassification(test_file, classifier_location + 'knn', 'knn')
        # update counts

        if result_knn[2][result_knn[0]] == 'np':
            knn_true_negative += 1
        else:
            knn_false_positive += 1

        if result_svm[2][int(result_svm[0])] == 'np':
            svm_true_negative += 1
        else:
            svm_false_positive += 1

    #move files back to main directory

    # We now have counts for all the measures
    num_svm_fn.append(svm_false_negative)
    num_svm_fp.append(svm_false_positive)
    num_svm_tn.append(svm_true_negative)
    num_svm_tp.append(svm_true_positive)

    num_knn_fn.append(knn_false_negative)
    num_knn_fp.append(knn_false_positive)
    num_knn_tn.append(knn_true_negative)
    num_knn_tp.append(knn_true_positive)

    for thing in glob.glob(p_holding_dir + '*.wav'):
        shutil.move(thing, p_directory)
    for thing in glob.glob(np_holding_dir + '*.wav'):
        shutil.move(thing, np_directory)

pickle.dump(num_train_set_list, open('num_train.p', 'wb'))

pickle.dump(num_svm_tp, open('svm_tp.p', 'wb'))
pickle.dump(num_svm_tn, open('svm_tn.p', 'wb'))
pickle.dump(num_svm_fp, open('svm_fp.p', 'wb'))
pickle.dump(num_svm_fn, open('svm_fn.p', 'wb'))

pickle.dump(num_knn_fp, open('knn_fp.p', 'wb'))
pickle.dump(num_knn_fn, open('knn_fn.p', 'wb'))
pickle.dump(num_knn_tn, open('knn_tn.p', 'wb'))
pickle.dump(num_knn_tp, open('knn_tp.p', 'wb'))

