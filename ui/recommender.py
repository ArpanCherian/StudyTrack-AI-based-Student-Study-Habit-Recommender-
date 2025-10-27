from django.db.models import Avg

def recommend_best_course(user, COURSES, studentdetails):
    enrolled_info = studentdetails.objects.filter(studentname=user.username)
    enrolled_names = set(e.coursename for e in enrolled_info)
    avg_result = enrolled_info.aggregate(completion_avg=Avg('completion'))
    avg_completion = avg_result['completion_avg'] or 0

    best_score = -1
    best_course = None
    for c in COURSES:
        if c['name'] in enrolled_names:
            continue
        total_enrolled = studentdetails.objects.filter(coursename=c['name']).count()
        completed = studentdetails.objects.filter(coursename=c['name'], status='Completed').count()
        completion_rate = (completed / total_enrolled * 100) if total_enrolled else 0
        score = completion_rate * 0.7 + total_enrolled * 0.15

        # Recommend short courses if user's avg completion is low
        try:
            months = int(c.get('duration', "1").split()[0])
        except Exception:
            months = 5
        if months <= 4 and avg_completion < 50:
            score += 10

        # Custom boosts: e.g. Python gets a bonus for new users
        if 'python' in c['name'].lower() and avg_completion < 25:
            score += 7

        if score > best_score:
            best_score = score
            best_course = c

    return best_course
