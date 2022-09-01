import twint as tw
import twint as tw
import numpy as np
import re
import pandas as pd
import streamlit as st
import datetime
import requests
import json
import certifi
import plotly.graph_objects as go


def setupTWINT(keyword,timeframe):
    # empty csv file
    f = open("twintOut.csv", "w")
    f.truncate()
    # set date
    today = datetime.date.today()
    sinceDate = today - datetime.timedelta(days=(timeframe))
    c = tw.Config()
    c.Lang = "en"
    c.Search = keyword
    c.Since = sinceDate.strftime("%Y-%m-%d")
    c.Store_json = True
    c.Lowercase = True
    c.Filter_retweets = True
    # c.Verified = True
    c.Pandas_clean = True
    c.Pandas = True
    c.Output = "twintOut.json"
    return c


# def addKeyword(oldKw):
# read input
#    newKw = readInput
#    keyword = oldkw + " OR " + newKw
#    return keyword

def setupStopwords():
    stopwords = ["a", "able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act",
                 "actually", "added", "adj",
                 "affected", "affecting", "affects", "after", "afterwards", "again", "against", "ah", "all", "almost",
                 "alone", "along",
                 "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "announce", "another",
                 "any", "anybody",
                 "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "apparently",
                 "approximately", "are", "aren",
                 "arent", "arise", "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away",
                 "awfully", "b", "back", "be",
                 "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin",
                 "beginning", "beginnings",
                 "begins", "behind", "being", "believe", "below", "beside", "besides", "between", "beyond", "biol",
                 "both", "brief", "briefly",
                 "but", "by", "c", "ca", "came", "can", "cannot", "can't", "cause", "causes", "certain", "certainly",
                 "co", "com", "come", "comes",
                 "contain", "containing", "contains", "could", "couldnt", "d", "date", "did", "didn't", "different",
                 "do", "does", "doesn't",
                 "doing", "done", "don't", "dont", "de", "down", "downwards", "due", "during", "e", "each", "ed", "edu",
                 "effect",
                 "eg", "eight", "eighty",
                 "either", "else", "elsewhere", "end", "ending", "enough", "especially", "et", "et-al", "etc", "even",
                 "ever", "every",
                 "everybody", "everyone", "everything", "everywhere", "ex", "except", "f", "far", "few", "ff", "fifth",
                 "first", "five", "fix",
                 "followed", "following", "follows", "for", "former", "formerly", "forth", "found", "four", "from",
                 "further", "furthermore",
                 "g", "gave", "get", "gets", "getting", "give", "given", "gives", "giving", "go", "goes", "gone", "got",
                 "gotten", "h", "had",
                 "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "hed", "hence", "her", "here",
                 "hereafter", "hereby",
                 "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him", "himself", "his",
                 "hither", "home", "how",
                 "howbeit", "however", "hundred", "i", "id", "ie", "if", "i'll", "im", "immediate", "immediately",
                 "importance", "important",
                 "in", "inc", "indeed", "index", "information", "instead", "into", "invention", "inwars", "is", "isn't",
                 "it", "itd", "it'll",
                 "its", "itself", "i've", "j", "just", "k", "keep", "keeps", "kept", "kg", "km", "know", "known",
                 "knows", "l", "largely", "last",
                 "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked",
                 "likely", "line", "little",
                 "'ll", "look", "looking", "looks", "ltd", "m", "made", "mainly", "make", "makes", "many", "may",
                 "maybe", "me", "mean", "means",
                 "meantime", "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "more", "moreover", "most",
                 "mostly", "mr", "mrs",
                 "much", "mug", "must", "my", "myself", "n", "na", "name", "namely", "nay", "nd", "near", "nearly",
                 "necessarily", "necessary",
                 "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "ninety", "no", "nobody",
                 "non", "none",
                 "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "now", "nowhere", "o",
                 "obtain", "obtained",
                 "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "ones",
                 "only", "onto", "or",
                 "ord", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over",
                 "overall", "owing",
                 "own", "p", "page", "pages", "part", "particular", "particularly", "past", "per", "perhaps", "placed",
                 "please", "plus",
                 "poorly", "possible", "possibly", "potentially", "pp", "predominantly", "present", "previously",
                 "primarily", "probably",
                 "promptly", "proud", "provides", "put", "q", "que", "quickly", "quite", "qv", "r", "ran", "rather",
                 "rd", "re", "readily",
                 "really", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related",
                 "relatively", "research",
                 "respectively", "resulted", "resulting", "results", "right", "run", "s", "said", "same", "saw", "say",
                 "saying", "says", "sec",
                 "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sent",
                 "seven", "several",
                 "shall", "she", "shed", "she'll", "shes", "should", "shouldn't", "show", "showed", "shown", "showns",
                 "shows", "significant",
                 "significantly", "similar", "similarly", "since", "six", "slightly", "so", "some", "somebody",
                 "somehow", "someone",
                 "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry",
                 "specifically", "specified",
                 "specify", "specifyingstill", "stop", "strongly", "sub", "substantially", "successfully", "such",
                 "sufficiently",
                 "suggest", "sup", "sure", "sv", "sy", "system", "sz", "t", "t's", "take", "taken", "taking", "tc",
                 "td", "tell", "ten",
                 "tends", "test", "text", "tf", "tg", "th", "than", "thank", "thanks", "thanx", "that", "that'll",
                 "that's", "that've",
                 "thatll", "thats", "thatve", "the", "their", "theirs", "them", "themselves", "then", "thence", "there",
                 "there'd", "there'll",
                 "there're", "there's", "there've", "thereafter", "thereby", "thered", "therefore", "therein",
                 "therell", "thereof", "therere",
                 "theres", "thereto", "thereupon", "thereve", "these", "they", "they'd", "they'll", "they're",
                 "they've", "theyd", "theyll",
                 "theyre", "theyve", "thick", "thin", "thing", "things", "think", "thinks", "third", "hirty", "this",
                 "thorough", "thoroughly",
                 "those", "thou", "though", "thoughh", "thought", "thoughts", "thousand", "three", "throug", "through",
                 "throughout", "thru",
                 "thus", "til", "till", "tip", "tis", "tj", "tk", "tm", "tn", "to", "today", "together", "too", "took",
                 "top", "toward", "towards", "tp",
                 "tr", "tried", "tries", "trillion", "truly", "try", "trying", "ts", "tt", "turn", "turned", "turning",
                 "turns", "tv", "tw", "twas",
                 "twelve", "twenty", "twice", "two", "tz", "u", "ua", "ug", "uk", "um", "un", "under", "underneath",
                 "undoing", "unfortunately",
                 "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "upward", "sus", "use", "used",
                 "useful", "usefully",
                 "usefulness", "uses", "using", "usually", "uucp", "uy", "uz", "v", "va", "value", "various", "vc",
                 "ve", "versus", "very", "vg",
                 "vi", "via", "viz", "vn", "vol", "vols", "vs", "vu", "w", "want", "wanted", "wanting", "wants", "was",
                 "wasn", "wasn't", "wasnt",
                 "way", "ways", "we", "we'd", "we'll", "we're", "we've", "web", "webpage", "website", "wed", "welcome",
                 "well", "wells", "went",
                 "were", "weren", "weren't", "werent", "weve", "wf", "what", "what'd", "what'll", "what's", "what've",
                 "whatever", "whatll", "whats",
                 "whatve", "when", "when'd", "when'll", "when's", "whence", "whenever", "where", "where'd", "where'll",
                 "where's", "whereafter",
                 "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether", "which", "whichever",
                 "while", "whilst", "whim",
                 "whither", "who", "who'd", "who'll", "who's", "whod", "whoever", "whole", "wholl", "whom", "whomever",
                 "whos", "whose", "why", "why'd",
                 "why'll", "why's", "widely", "width", "will", "willing", "wish", "with", "within", "without", "won",
                 "won't", "wonder", "wont", "words",
                 "work", "worked", "working", "works", "world", "would", "would've", "wouldn", "wouldn't", "wouldnt",
                 "ws", "www", "x", "y", "ye", "year",
                 "years", "yes", "yet", "you", "you'd", "you'll", "you're", "you've", "youd", "youll", "young",
                 "younger", "youngest", "your", "youre",
                 "yours", "yourself", "yourselves", "youve", "yt", "yu", "z", "za", "zero", "zm", "zr", "still", "love",
                 "june", "july", "august", "september", "october", "november", "december", "hours", "minutes", "days",
                 "feel", "going", "free", "profit"]
    # specific itsec stopwords
    itsecStop = ["cyber", "threat", "threats", "vulnerabilities", "false", "zero", "itsecurity", "update", "network",
                 "hacker", "check","inkhallows","initiative","en","watch","hope","la","man","execution",
                 "security", "vulnerability", "zeroday", "0day", "patchday", "itsec", "itsecurity", "networksecurity",
                 "cyberattack", "cyberattacks","coming", "andre","art","crypto","best","amazing","better","don","morning","lol","business",
                 "agnostic", "intelligence", "precrime", "domain", "siem", "code", "code", "join", "anonymous", "kako",
                 "patch tuesday",
                 "hacktivist", "exploit", "predicted", "https", "http", "near", "youtube", "critical", "people",
                 "google",
                 "want", "last", "data", "organisation", "organization", "phishing", "habib rizieq", "habib", "rizieq",
                 "cybersecurity",
                 "malicious", "cybercrime", "domains", "netsec", "come", "ransomware", "tech", "malware", "make",
                 "read", "infosec",
                 "make", "help", "cyberthreat", "bugbounty", "positives cyberthreat", "report", "patch", "advice",
                 "need",
                 "threatintelligence", "sysadmin", "admin", "attack", "good", "time", "gore", "ransomware", "windows",
                 "patches",
                 "remote", "unauthenticated", "injection", "group", "politik", "politic", "politics", "tuesday",
                 "privacy", "russia",
                 "microsoft", "positives", "Catalog", "avoid", "issue", "Execution", "known", "spoofing", "controller",
                 "attacker",
                 "vuln", "risk", "service", "publishing", "exploited", "flaw", "exploitation", "error", "cooperation",
                 "different", "added",
                 "known", "issues", "actively", "controllers", "default", "pulled", "will", "available", "great",
                 "cisa", "first,""cisagov", "cves",
                 "updates", "active", "services", "LDAP", "enterprise", "securitynews", "technically", "ranked",
                 "large", "work", "research",
                 "including", "right", "networks", "learn", "infosecurity", "significant", "authentication", "guidance",
                 "failures", "party", "applied", "used"
                                                 "payload", "threatintel", "include", "device", "project", "public",
                 "bug", "zero-day", "warns", "https: // t", "i'm", "vendors", "agencies", "pull",
                "cve", "federal", "android", "apple", "bugs", "0-day", "0-days", "days", "spyware", "exploit",
                 "exploits", "day", "0", "-", "alleviate", "burden", "storyline",
                "avg", "response", "amp", "deaths", "attacks", "teams", "week", "ago", "urges", "raw", "predator",
                "flaws", "list", "adds", "xr", "ios", "agency", "us", "fest"
    , "hacked", "safari", "pwn", "webcast", "mass", "shooting","shit","draw","cp","hackers","hacking","tag","zeroday__","es","el",
                 "book", "news","video","imluxu","thisisradinsky","lot","full","life","lt","teudipikanyaho","countdown","bad","wiflbaby",
                "por","su","vulnerabilit","cuba","crew","perillamint","fox","steal","bitcoin"]
    stopwords.extend(itsecStop)
    return stopwords


def updateWordFreq(newStop, varFrequencyList):
    newStopwords.append(newStop)
    retFrequencyList = varFrequencyList.drop(labels=[newStop])

    return retFrequencyList


def getNewStopwords():
    return newStopwords


# def update_df():
#    c.Resume = "twintOut.csv"


def filter_df(variable_df):
    filter_df = variable_df.filter(items=['tweet', 'username', 'name', 'hashtags', 'language', 'nretweets', 'nlikes'])
    filter_df = filter_df.sort_values(by='nlikes', ascending=False)
    return filter_df


def getWordFrequency(variableDataframe):
    # turn all tweets into a string and remove the stopwords
    asciiGone = variableDataframe.tweet.str.encode('ascii', 'ignore').str.decode('ascii')
    tweetStrip = asciiGone.str.strip('[]').str.replace(r'\W+', ' ').str.replace(r'\d', ' ').str.split(',')

    listOfTweets = list(set([a.lower() for b in tweetStrip for a in b]))
    resultWords = [word for line in listOfTweets for word in line.split() if word not in stopwords]

    # count frequency

    word_freq = pd.value_counts(np.array(resultWords))
    word_freq.columns = ['Word', 'Frequency']
    # col1.bar_chart(word_freq)
    return word_freq


def getCVECodes(variableDataframe):
    # turn df into string and extract cve codes
    tweetWords = list(set([a.lower() for b in variableDataframe.tweet.str.split(' ') for a in b]))
    cveTweets = list(set(word for word in tweetWords if "cve-" in word))
    cvesList = []
    for word in cveTweets:
        word = word.partition("cve-")
        # sanity check for word[2][0:10]
        cvesList.append(word[1] + word[2][0:10])
        # count frequency

    print(cvesList)
    return cvesList


def countCVEfreq(cveCodes):
    cve_freq = pd.value_counts(np.array(cveCodes))
    cve_freq.columns = ['Word', 'Frequency']
    return cve_freq


def getJSONInfo(cvecode):
    url = "https://services.nvd.nist.gov/rest/json/cve/1.0/" + str(cvecode)
    urlReq = requests.get(url)
    try:
        data = json.loads(urlReq.text)
        if "result" in data:
            return str([data["result"]["CVE_Items"][0]["cve"]["description"]["description_data"][0]["value"]])
        else:
            return
    except json.decoder.JSONDecodeError:
            return


def getCVEOutput():
    cveList = getCVECodes(tweets_df)
    countedCode = countCVEfreq(cveList)
    topcveDescription = []
    topListcve = []
    marklist = list(reversed(sorted(countedCode.items(), key=lambda x: x[1])))
    print(topListcve)
    #marklist = list(sorted(countedCode.items(), key=lambda x: x[1]))
    for x in marklist:
        if int("".join(filter(str.isdecimal, x[0])) + "0") > 20009990 :
            topListcve.append(x[0])
            topcveDescription.append(getJSONInfo(x[0]))
    cveDict = pd.DataFrame(zip(topListcve, topcveDescription))
    cveDF = pd.DataFrame(cveDict)
    cveDF.columns = ["CVE ID", "Description"]
    return (cveDF)




def useCSV():
    # df = pd.read_csv('twintOut.csv')
    df = pd.read_json('twintOut.json', lines=True)

    return df


# start
st.set_page_config(layout="wide")
col1, col2, col3 = st.columns(3)
col4,col5 = st.columns(2)
col6,col7 = st.columns(2)



st.subheader('''Cyber Trends''')
col1.subheader("last 24 hours")
col2.subheader("Last 7 days")
col3.subheader("last 30 days")

with col6:
    with st.form(key="Stopword_Form"):
        newStop = st.text_input("Add new Stopword: ")
        submitButtonStop = st.form_submit_button(label="Add")

with col7:
    with st.form(key="Keyword"):
        newKeyword = st.text_input("Search for specific Term ")
        submitButtonKw = st.form_submit_button(label="Search")
        

st.subheader("CVEs")

stopwords = setupStopwords()
newStopwords = []
keyword = "zeroday" or "0day" or "0-day" "zero-day" or "0-days" or "cve"


#24 Stunden Search

c = setupTWINT(keyword,1)
tw.run.Search(c)
tweets_df = tw.storage.panda.Tweets_df
frequencyList = getWordFrequency(tweets_df)
col1.text(frequencyList[:9])



#30 Tage Search

c = setupTWINT(keyword,30)
tw.run.Search(c)
tweets_df = tw.storage.panda.Tweets_df
frequencyList = getWordFrequency(tweets_df)
col3.text(frequencyList[:9])


#7 Tage Search 

c = setupTWINT(keyword,7)
tw.run.Search(c)
##marklist = list(reversed(sorted(countedCode.items(), key=lambda x: x[1])))
tweets_df = tw.storage.panda.Tweets_df

# tweets_df = useCSV()
# filteredDataframe = filter_df(tweets_df)
frequencyList = getWordFrequency(tweets_df)
#fig = go.Figure(
#    go.Pie(
#    labels = frequencyList["Word"].toList(),
#    values = frequencyList["Frequency"].toList(),
#    hoverinfo = "Word+Frequency",
#    textinfo = "Frequency"
#))
col2.text(frequencyList[:9])

cveOut=getCVEOutput()
st.table(cveOut)
# run conditions


if submitButtonStop:
    col2.text(updateWordFreq(newStop, frequencyList[:9]))

if submitButtonKw:
    c = setupTWINT(newKeyword,7)
    tw.run.Search(c)
    tweets_df = tw.storage.panda.Tweets_df
    frequencyList = getWordFrequency(tweets_df)
    col4.write(frequencyList[:9])
