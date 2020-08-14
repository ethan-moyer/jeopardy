from bs4 import BeautifulSoup
import requests

class ArchiveParser():
    def __init__(self, game_id):
        self.game_id = game_id
    
    def get_first_set(self):
        """Returns a dictionary containing categories, questions, and answers for the first round."""

        questions_url = "http://www.j-archive.com/showgame.php?game_id=" + self.game_id
        answers_url = "http://www.j-archive.com/showgameresponses.php?game_id=" + self.game_id
        data = { "categories": [], "questions": [], "answers": [] }

        page = requests.get(questions_url)
        soup = BeautifulSoup(page.text, "html.parser")

        for category in soup.find_all(class_="category_name")[:6]:
            data["categories"].append(category.text)

        for row in range(5):
            data["questions"].append([])
            for col in range(6):
                try:
                    data["questions"][row].append(soup.find(id="clue_J_{x}_{y}".format(x=col+1, y=row+1)).text)
                except:
                    data["questions"][row].append(None)
        
        page = requests.get(answers_url)
        soup = BeautifulSoup(page.text, "html.parser")
        answers = soup.find_all(class_="correct_response")
        i = 0

        for row in range(5):
            data["answers"].append([])
            for col in range(6):
                if data["questions"][row][col] is None:
                    data["answers"][row].append(None)
                else:
                    data["answers"][row].append(answers[i].text)
                    i += 1

        return data

    def get_second_set(self):
        """Returns a dictionary containing categories, questions, and answers for the second round."""

        questions_url = "http://www.j-archive.com/showgame.php?game_id=" + self.game_id
        answers_url = "http://www.j-archive.com/showgameresponses.php?game_id=" + self.game_id
        data = { "categories": [], "questions": [], "answers": [] }

        page = requests.get(questions_url)
        soup = BeautifulSoup(page.text, "html.parser")

        for category in soup.find_all(class_="category_name")[6:12]:
            data["categories"].append(category.text)

        for row in range(5):
            data["questions"].append([])
            for col in range(6):
                try:
                    data["questions"][row].append(soup.find(id="clue_DJ_{x}_{y}".format(x=col+1, y=row+1)).text)
                except:
                    data["questions"][row].append(None)
        
        page = requests.get(answers_url)
        soup = BeautifulSoup(page.text, "html.parser")
        div = soup.find(id="double_jeopardy_round")
        answers = div.findChildren(class_="correct_response", recursive=True)
        i = 0

        for row in range(5):
            data["answers"].append([])
            for col in range(6):
                if data["questions"][row][col] is None:
                    data["answers"][row].append(None)
                else:
                    data["answers"][row].append(answers[i].text)
                    i += 1

        return data

if __name__ == "__main__":
    ap = ArchiveParser("6589")
    print(ap.get_second_set())