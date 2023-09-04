from django.shortcuts import render, redirect
from django.conf import settings 
from django.http import HttpResponse
from .models import *

# Create your views here.
def calculate_rating(hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)
    total_review = max(Review.objects.filter(hospital=hospital).count(), 1)
    positive_review = Review.objects.filter(hospital=hospital, label="positive").count()
    return positive_review/total_review * 100

def rating_view(request):
    hospitals = list(Hospital.objects.all())

    for i in range(len(hospitals)):
        hospitals[i] = hospitals[i].__dict__

    for h in hospitals:
        h['rating'] = calculate_rating(h['id'])
        h['number_of_reviews'] = Review.objects.filter(hospital=h['id']).count()
    
    hospitals = sorted(hospitals, key=lambda x: x["rating"], reverse=True)
    return render(request, "rating_template.html", context={
        "hospital_with_rating" : hospitals,
    })


def review_view(request):
    if Hospital.objects.count() == 0:
        return HttpResponse("No hospitals added")

    cur_hospital = request.GET.get("id", Hospital.objects.first().id)
    if Hospital.objects.filter(id=cur_hospital).exists() == False:
        return HttpResponse("No hospital exists with the given id.")

    if request.method == 'POST':
    
        hospital = Hospital.objects.get(id = request.POST.get("hospital_id")) 
        review = request.POST.get("review")

        result = settings.SVM_MODEL.predict([review])
        # print(result[0])
        Review.objects.create(hospital=hospital, review_text=review, label=result[0])

        return redirect(f"/hospital/?id={cur_hospital}")


    total_review = Review.objects.filter(hospital=cur_hospital).count()
    positive_review = Review.objects.filter(hospital=cur_hospital, label="positive").count()

    if total_review == 0:
        total_review = 1
    
    return render(request, "review_template.html", context={
        "all_hospitals" : Hospital.objects.all(),
        "hospital" : Hospital.objects.get(id=cur_hospital),
        "reviews" : Review.objects.filter(hospital=cur_hospital).order_by("-created_at"),
        "positive_percentage" : positive_review/total_review * 100
    })