import requests
import json
from tqdm.auto import tqdm

query = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    boundTopicId
    title
    titleSlug
    content
    translatedTitle
    translatedContent
    isPaidOnly
    difficulty
    likes
    dislikes
    isLiked
    similarQuestions
    exampleTestcases
    categoryTitle
    contributors {
      username
      profileUrl
      avatarUrl
      __typename
    }
    topicTags {
      name
      slug
      translatedName
      __typename
    }
    companyTagStats
    codeSnippets {
      lang
      langSlug
      code
      __typename
    }
    stats
    hints
    solution {
      id
      canSeeDetail
      paidOnly
      hasVideoSolution
      paidOnlyVideo
      __typename
    }
    status
    sampleTestCase
    metaData
    judgerAvailable
    judgeType
    mysqlSchemas
    enableRunCode
    enableTestMode
    enableDebugger
    envInfo
    libraryUrl
    adminUrl
    challengeQuestion {
      id
      date
      incompleteChallengeCount
      streakCount
      type
      __typename
    }
    __typename
  }
}
"""

ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"
ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"
algorithms_problems_json = requests.get(ALGORITHMS_ENDPOINT_URL).content
algorithms_problems_json = json.loads(algorithms_problems_json)

links = []
for child in algorithms_problems_json["stat_status_pairs"]:
        # Only process free problems
        if not child["paid_only"]:
            question__title_slug = child["stat"]["question__title_slug"]
            question__article__slug = child["stat"]["question__article__slug"]
            question__title = child["stat"]["question__title"]
            frontend_question_id = child["stat"]["frontend_question_id"]
            difficulty = child["difficulty"]["level"]
            links.append((question__title_slug, difficulty, frontend_question_id, question__title, question__article__slug))
            
links = sorted(links, key=lambda x: (x[2]))

url = 'https://leetcode.com/graphql'

for title_slug, difficulty, question_id, question_title, article_slug in tqdm(links):
    variables = {"titleSlug": title_slug}
    r = requests.post(url, json={'query': query , 'variables': variables})
    print(r.status_code)
    res = json.loads(r.text)

    with open(f"json/LC{question_id}.json", "w") as f:
        json.dump(res, f)