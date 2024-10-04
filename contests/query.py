from django.contrib.auth import get_user_model
from django.db.models import Q, Max, F
from django.shortcuts import get_object_or_404
from problems.models import Submission

from .models import Contest

User = get_user_model()


def list_problems(contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    return contest.problems.all()


def list_users(contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    return contest.participants.all()


def list_submissions(contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    return Submission.objects.filter(problem__in=contest.problems.all()).order_by(
        "-submitted_time"
    )


def list_problem_submissions(contest_id, problem_id):
    participants = Contest.objects.get(id=contest_id).participants.all()
    return Submission.objects.filter(
        problem_id=problem_id, participant__in=participants
    ).order_by("-submitted_time")


def list_user_submissions(contest_id, user_id):
    return Submission.objects.filter(
        Q(problem__contest__id=contest_id) & Q(participant__id=user_id)
    ).order_by("-submitted_time")


def list_problem_user_submissions(contest_id, user_id, problem_id):
    return Submission.objects.filter(
        Q(problem__contest__id=contest_id)
        & Q(participant__id=user_id)
        & Q(problem__id=problem_id)
    ).order_by("-submitted_time")


def list_users_solved_problem(contest_id, problem_id):
    return User.objects.filter(
        Q(submissions__problem_id=problem_id) &
        Q(submissions__problem__contest__id=contest_id) &
        Q(submissions__score=F('submissions__problem__score'))
    ).distinct().order_by('-submissions__submitted_time')


def user_score(contest_id, user_id):
    submissions_score = (
        Submission.objects.filter(
            Q(problem__contest__id=contest_id) & Q(participant__id=user_id)
        )
        .values("problem_id")
        .annotate(Max("score"))
    )
    return sum(submission["score__max"] for submission in submissions_score)


def list_final_submissions(contest_id):
    return (
        Submission.objects.filter(Q(problem__contest__id=contest_id))
        .values("participant_id", "problem_id")
        .annotate(Max("score"))
        .order_by("participant_id")
    )