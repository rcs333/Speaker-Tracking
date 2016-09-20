import glob
import subprocess

"""
Ryan's Annotation program:

I'll set up a huge amount of files, so when you hit run the first one will play
    Run is either the little green triangle in the top right or Ctrl-Shift-F10

Type in your annotation and hit the return key and a new one will play

To replay append 1 <- (The number one) to your annotation

You can start typing as soon as the playing starts although you won't be able to see it, it'll still get recorded

If the file is just noise or incomprehensible type in <noise>

If the file doesn't play and there's an error like 'Under-Run' just hit enter and move to the next file.

You can stop anytime you like by either just leaving the program running, or hitting the red square (progress *should*
    be saved)

slang should be typed exactly as it is said i.e. 'gonna' 'wanna' ect. swearwords are important too!

As a general rule, incomplete annotations are worse than skipping one so keep that in mind, although you can let me know
    or write a message with {message} which I'll run into when I'm processing your annotations.


My number is (509)-823-9676 if anything horrendous happens or you have lexical or other questions.

Please let me know if you hate using this program to annotate and I can hook you up with either improvements to this code
or some other options, If you find some other program online or something and you want to use let me know as well.
"""


output_file = '/home/ryan/output.txt'
file_dir = '/home/ryan/Desktop/ToSort/AW/Alice_9be790ba-0f15-4687-94e5-f02ee50d07a8_0271.wav/*'


def transcribe(filepath, string):
    subprocess.call('play ' + filepath, shell=True)
    print('Transcription:\n' + string + '\n')
    input = raw_input('Enter transcription:')
    string = string + ' ' + input
    if string[-1] == '1':
        return transcribe(filepath, string[:-1])
    else:
        return string

# replay
# quiting

if __name__ == '__main__':

    for file_path in sorted(glob.glob(file_dir)):
        trans = transcribe(file_path, '')
        subprocess.call('echo \'' + file_path + '\t' + trans + '\' >> ' + output_file,shell=True)
        subprocess.call('mv ' + file_path + ' /home/ryan/done', shell=True)

