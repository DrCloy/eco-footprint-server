from datetime import datetime

from core.model import ItemState
from core.repo import ChallengeRepository
from util.adVerifier import AdVerifier


async def check_ad_log(adVerifier: AdVerifier):
    await adVerifier.remove_old_log()

    return


def check_challenge_expiry(challengeRepository: ChallengeRepository):
    challenges = challengeRepository.getAllChallenges()
    for challenge in challenges:
        if int(challenge.dateEnd) < datetime.now().timestamp():
            challenge_detail = challengeRepository.getChallenge(challenge.id)
            challenge_detail.state = ItemState.FINISHED
            challengeRepository.updateChallenge(challenge_detail)

    return
