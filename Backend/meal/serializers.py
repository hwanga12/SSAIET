from rest_framework import serializers


# ======================================================
# 📅 캘린더 월 조회용 (요약 Serializer)
# ======================================================

class LunchCalendarSerializer(serializers.Serializer):
    meal_name = serializers.CharField()
    course_type = serializers.CharField()


class DinnerCalendarSerializer(serializers.Serializer):
    ai_menu_name = serializers.CharField(allow_null=True)
    is_eaten = serializers.BooleanField(allow_null=True)


class CalendarDaySerializer(serializers.Serializer):
    date = serializers.IntegerField()
    lunch = LunchCalendarSerializer(required=False, allow_null=True)
    dinner = DinnerCalendarSerializer(required=False, allow_null=True)


# ======================================================
# 📄 날짜 상세 조회용 (Detail Serializer)
# ======================================================

class LunchDetailSerializer(serializers.Serializer):
    meal_name = serializers.CharField()
    course_type = serializers.CharField()
    restaurant = serializers.CharField()
    subMenuTxt = serializers.CharField(allow_null=True)
    p_score = serializers.IntegerField()
    photoUrl = serializers.URLField(allow_null=True)


class DinnerDetailSerializer(serializers.Serializer):
    ai_menu_name = serializers.CharField(allow_null=True)
    ai_reason_text = serializers.CharField(allow_null=True)
    p_score = serializers.FloatField()
    is_eaten = serializers.BooleanField(allow_null=True)


class NutritionDayDetailSerializer(serializers.Serializer):
    date = serializers.IntegerField()
    lunch = LunchDetailSerializer(allow_null=True)
    dinner = DinnerDetailSerializer(allow_null=True)
