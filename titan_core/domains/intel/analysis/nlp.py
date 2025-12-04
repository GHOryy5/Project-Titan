class SentimentEngine:
    def __init__(self):
        self.threat_lexicon = ["bomb", "attack", "midnight", "package", "eagle"]
        
    def analyze_comms(self, transcript):
        score = 0
        hits = []
        words = transcript.lower().split()
        for w in words:
            if w in self.threat_lexicon:
                score += 10
                hits.append(w)
        return score, hits
