import urllib.request
import re
import sys

def find_urls(source_code):
    url_list = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', source_code)
    return url_list;


def find_emails(source_code):
    emails_list = re.findall(r'[\w\.-]+@[\w\.-]+', source_code)
    return emails_list


def search(ext_list, extension):
    st = 0
    end = len(ext_list) - 1

    while(st <= end):
        mid = st + (end-st)//2

        if extension == ext_list[mid]: return True

        if ext_list[mid] > extension:
            end = mid - 1
        else:
            st = mid + 1

    return False


def is_correct_url(url):
    url_components = url.split('.')

    if len(url_components) == 0:
        return False

    extension = url_components[len(url_components)-1]
    extension = extension.strip('\n')
    extension = extension.lower()

    ext_list = ['aac', 'ai', 'amr', 'avi', 'bat', 'css', 'csv', 'dat', 'docx', 'esp', 'flv', 'gif', 'jpeg', 'jpf', 'jpg', 'js', 'json', 'm4r', 'mkv', 'mp2', 'mp3', 'mp4', 'mpeg', 'mpv', 'ogg', 'pcap', 'pdf', 'png', 'ppt', 'psd', 'py', 'svg', 'tiff', 'txt', 'wav', 'wma', 'wmv']

    if search(ext_list, extension):
        return False

    return True


def file_handling(data, file_name):
    with open(file_name, 'a+', encoding='utf-8') as file:
        for line in data:
            file.write(line + '\n')


def email_fetch(urls_file_name):
    file_name = 'emails.txt'
    emails_set = set()

    with open(urls_file_name, 'r', encoding='utf-8') as urls_file:
        for url in urls_file.readlines():
            print(f'Processing {url}', end='')

            if is_correct_url(url):
                try:
                    response = urllib.request.Request(
                        url,
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
                        }
                    )
                    response_data = urllib.request.urlopen(response)
                except urllib.error.HTTPError as e:
                    print(f'HTTPError: {e.code}')
                    print('Processing next...')
                except urllib.error.URLError as e:
                    print(f'URLError: {e.reason}')
                    print('Processing next...')
                else:
                    try:
                        html_byte = response_data.read()
                        source_code = html_byte.decode('utf-8')
                        emails_list = find_emails(source_code)

                        for email in emails_list:
                            emails_set.add(email)
                    except:
                        print(f'Invalid url {url}')
                        print('Processing next...')
            else:
                print(f'Invalid url {url}')
                print('Processing next...')

    file_handling(emails_set, file_name)

    print('Completed Successfully')


def main():
    url = input('Enter a web url: ')

    try:
        response = urllib.request.Request (
            url,
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
            }
        )

        response_data = urllib.request.urlopen(response)
    except urllib.error.HTTPError as e:
        print(f'HTTPError: {e.code}')
        sys.exit()
    except urllib.error.URLError as e:
        print(f'URLError: {e.reason}')
        sys.exit()
    else:
        html_byte = response_data.read()
        source_code = html_byte.decode('utf-8')
        urls_list = find_urls(source_code)

        file_name = 'urls.txt'
        file_handling(urls_list, file_name)
        email_fetch(file_name)


if __name__ == '__main__':
    main()