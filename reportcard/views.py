from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .models import (
    ReportCard,
    SubjectScore,
    AffectiveDisposition,
    PsychomotorSkill,
    Term,
    Class,
    Subject,
)

from .forms import (
    ReportCardForm,
    SubjectScoreFormSet,
    AffectiveDispositionForm,
    PsychomotorSkillForm,
)


@login_required
def report_card_list(request):
    report_cards = ReportCard.objects.select_related('student', 'term')

    term_filter = request.GET.get('term')
    class_filter = request.GET.get('class')

    if term_filter:
        report_cards = report_cards.filter(term_id=term_filter)

    if class_filter:
        report_cards = report_cards.filter(student__student_class_id=class_filter)

    return render(request, 'reportcard/report_card_list.html', {
        'report_cards': report_cards,
        'terms': Term.objects.all(),
        'classes': Class.objects.all(),
    })


@login_required
def create_report_card(request):
    if request.method == 'POST':
        form = ReportCardForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                report_card = form.save()

                for subject in Subject.objects.all():
                    SubjectScore.objects.create(
                        report_card=report_card,
                        subject=subject
                    )

                AffectiveDisposition.objects.create(report_card=report_card)
                PsychomotorSkill.objects.create(report_card=report_card)

                messages.success(request, 'Report card created successfully.')
                return redirect('edit_report_card', pk=report_card.pk)
    else:
        form = ReportCardForm()

    return render(request, 'reportcard/report_card_form.html', {'form': form})


@login_required
def edit_report_card(request, pk):
    report_card = get_object_or_404(ReportCard, pk=pk)

    if request.method == 'POST':
        form = ReportCardForm(request.POST, instance=report_card)
        subject_formset = SubjectScoreFormSet(request.POST, instance=report_card)
        affective_form = AffectiveDispositionForm(request.POST, instance=report_card.affective)
        psychomotor_form = PsychomotorSkillForm(request.POST, instance=report_card.psychomotor)

        if all([
            form.is_valid(),
            subject_formset.is_valid(),
            affective_form.is_valid(),
            psychomotor_form.is_valid()
        ]):
            with transaction.atomic():
                form.save()
                subject_formset.save()
                affective_form.save()
                psychomotor_form.save()

                messages.success(request, 'Report card updated.')
                return redirect('view_report_card', pk=pk)
    else:
        form = ReportCardForm(instance=report_card)
        subject_formset = SubjectScoreFormSet(instance=report_card)
        affective_form = AffectiveDispositionForm(instance=report_card.affective)
        psychomotor_form = PsychomotorSkillForm(instance=report_card.psychomotor)

    return render(request, 'reportcard/report_card_edit.html', {
        'form': form,
        'subject_formset': subject_formset,
        'affective_form': affective_form,
        'psychomotor_form': psychomotor_form,
        'report_card': report_card,
    })


@login_required
def view_report_card(request, pk):
    report_card = get_object_or_404(ReportCard, pk=pk)

    return render(request, 'reportcard/report_card_view.html', {
        'report_card': report_card,
        'subject_scores': report_card.subject_scores.select_related('subject'),
    })


@login_required
def delete_report_card(request, pk):
    report_card = get_object_or_404(ReportCard, pk=pk)

    if request.method == 'POST':
        report_card.delete()
        messages.success(request, 'Report card deleted.')
        return redirect('report_card_list')

    return render(request, 'reportcard/report_card_confirm_delete.html', {
        'report_card': report_card
    })
