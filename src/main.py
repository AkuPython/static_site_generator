import os
import shutil
import helper_functions


def clean_public(folder=''):
    src = 'static'
    dst = 'public'
    j = lambda directory: '/'.join(directory).replace('//', '/')
    if folder == '':
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.mkdir(dst)
    else:
        os.mkdir(j([dst, folder]))
    if not os.path.exists(src):
        raise Exception(f'Where is {src}??')
    for item in os.listdir(j([src, folder])):
        if os.path.isfile(j([src, folder, item])):
            shutil.copy(j([src, folder, item]), j([dst, folder, item]))
        else:
            clean_public(j([folder + item]))


def main():
    clean_public()
    helper_functions.generate_pages_recursive('content', 'template.html', 'public')


main()

