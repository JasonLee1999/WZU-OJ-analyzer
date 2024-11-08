from typing import OrderedDict
import pandas
from datetime import datetime, timedelta


class Submission:
    def __init__(self, id, name, class_name, problem_id, submission_time):
        self.id = int(id)
        self.name: str = name
        self.class_name: str = class_name
        self.problem_id = int(problem_id)
        self.submission_time = datetime.strptime(submission_time, "%Y-%m-%d,%H:%M:%S")

    def __eq__(self, other):
        if not isinstance(other, Submission):
            return NotImplemented

        return (
            self.name == other.name
            and self.class_name == other.class_name
            and self.problem_id == other.problem_id
        )

    def __hash__(self):
        return hash((self.name, self.class_name, self.problem_id))


class User:
    def __init__(self, name, class_name):
        self.name: str = name
        self.class_name: str = class_name
        self.submissions: list[Submission] = []
        self.rating: float = 0
        self.time_bonus_sum: float = 0
        self.time_bonus_cnt: int = 0


class Problem:
    def __init__(self, problem_id):
        self.users_id: list[tuple[str, str]] = []
        self.problem_id: int = problem_id
        self.time_sum: float = 0.0
        self.trust_time_len: int = 0
        self.len: int = 0
        self.diff: float = 0.0

    def time_ave(self):
        len = self.trust_time_len
        time_ave_true = int(self.time_sum / 60 / len) if len != 0 else 20
        return (time_ave_true * len + 200) / (len + 10)


ori_submissions: list[Submission] = []
uni_submissions: list[Submission] = []
excel_path = "submission_data.xlsx"
data_frame = pandas.read_excel(excel_path)
for index, row in data_frame.iterrows():
    submission = Submission(
        id=row["id"],
        name=row["name"],
        class_name=row["class"],
        problem_id=row["problem"],
        submission_time=row["time"],
    )
    ori_submissions.append(submission)
ori_submissions.reverse()
uni_submissions = list(OrderedDict.fromkeys(ori_submissions))
users: dict[tuple[str, str], User] = {}
for submission in uni_submissions:
    key = (submission.name, submission.class_name)
    if key not in users:
        users[key] = User(name=submission.name, class_name=submission.class_name)
    users[key].submissions.append(submission)
users_val = sorted(users.values(), key=lambda user: len(user.submissions), reverse=True)

problems: dict[int, Problem] = {}
for user in users_val:
    past = None
    for submission in user.submissions:
        key = submission.problem_id
        if key not in problems:
            problems[key] = Problem(problem_id=submission.problem_id)
        problem = problems[key]
        if past == None:
            past = submission.submission_time
            submission.submission_time = None
        else:
            if submission.submission_time - past < timedelta(hours=1):
                delta = (submission.submission_time - past).total_seconds()
                problem.time_sum += delta
                problem.trust_time_len += 1
                past = submission.submission_time
                submission.submission_time = delta
            else:
                past = submission.submission_time
                submission.submission_time = None
        problem.len += 1
        problem.users_id.append((submission.name, submission.class_name))

        problem.diff = (1 - (problem.time_ave()) / 60) * (problem.len + 5) / 250
problems_val = sorted(problems.values(), key=lambda problem: problem.diff, reverse=True)

problems_data = [
    {
        "ID": problem.problem_id,
        "Time_ave": int(problem.time_ave()),
        "AC_sum": problem.len,
        "diff": problem.diff,
        **{
            f"{user_name}, {class_name}": "AC"
            for user_name, class_name in problem.users_id
        },
    }
    for problem in problems_val
]
data_frame = pandas.DataFrame(problems_data)
excel_output_path = "problems_data.xlsx"
data_frame.to_excel(excel_output_path, index=False)
print(f"数据已保存到Excel文件:{excel_output_path}")

for user_id in users:
    key = user_id
    user = users[key]
    sum = 0
    for i in range(len(user.submissions)):
        sum += pow(0.95 * 0.95, i + 1)
    user.rating = 0
    user.submissions.sort(key=lambda sub: problems[sub.problem_id].diff)
    k = 0
    for submission in user.submissions:
        k += 1
        problem = problems[submission.problem_id]
        if problem.trust_time_len >= 5 and submission.submission_time != None:
            now_minutes = submission.submission_time / 60
            time_ave = problem.time_sum / 60 / problem.trust_time_len
            if now_minutes > time_ave:
                delta = 35 - time_ave
                time_ave += delta
                now_minutes += delta
            elif now_minutes < time_ave:
                delta = 35 - now_minutes
                time_ave += delta
                now_minutes += delta
            time_bonus = time_ave / now_minutes
            user.time_bonus_cnt += 1
            user.time_bonus_sum += time_bonus
    k = 0
    for submission in user.submissions:
        k += 1
        problem = problems[submission.problem_id]
        coef = 1.0
        if user.time_bonus_cnt >= 1:
            coef = user.time_bonus_sum / user.time_bonus_cnt
        user.rating += pow(0.95, k) * (1 - problem.diff) * coef
    user.rating = user.rating / sum * 100
sorted_users = sorted(users_val, key=lambda user: user.rating, reverse=True)

data = [
    {
        "Name": user.name,
        "Class": user.class_name,
        "AC_Sum": len(user.submissions),
        "Time_Bonus": (
            (user.time_bonus_sum / user.time_bonus_cnt)
            if user.time_bonus_cnt >= 1
            else 1.0
        ),
        "Rating": user.rating,
    }
    for user in sorted_users
]
df_users = pandas.DataFrame(data)
excel_output_path = "sorted_users.xlsx"
df_users.to_excel(excel_output_path, index=False)
print(f"数据已保存到Excel文件:{excel_output_path}")
