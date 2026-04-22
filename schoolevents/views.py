from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import SchoolEvent, EventGallery, EventDocument
from .forms import EventGalleryForm, EventDocumentForm




class EventListView(ListView):
    model = SchoolEvent
    template_name = "events/event_list.html"
    context_object_name = "events"


class EventDetailView(DetailView):
    model = SchoolEvent
    template_name = "events/event_detail.html"
    context_object_name = "event"


def upload_gallery(request, pk):
    event = get_object_or_404(SchoolEvent, pk=pk)

    if request.method == "POST":
        form = EventGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_item = form.save(commit=False)
            gallery_item.event = event
            gallery_item.save()
            return redirect("event_detail", pk=event.pk)
    else:
        form = EventGalleryForm()

    return render(request, "events/gallery_upload.html", {"form": form, "event": event})



# --------- DOCUMENT UPLOAD VIEW ----------
def upload_document(request, pk):
    event = get_object_or_404(SchoolEvent, pk=pk)

    if request.method == "POST":
        form = EventDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.event = event
            doc.save()
            return redirect("event_detail", pk=event.pk)
    else:
        form = EventDocumentForm()

    return render(request, "events/document_upload.html", {
        "form": form,
        "event": event
    })


class EventCreateView(CreateView):
    model = SchoolEvent
    fields = [
        'event_type', 'title', 'description', 'academic_year',
        'start_date', 'end_date', 'cover_image', 'venue',
        'organizers', 'is_published'
    ]
    template_name = "events/event_form.html"
    success_url = reverse_lazy("event_list")


class EventUpdateView(UpdateView):
    model = SchoolEvent
    fields = [
        'event_type', 'title', 'description', 'academic_year',
        'start_date', 'end_date', 'cover_image', 'venue',
        'organizers', 'is_published'
    ]
    template_name = "events/event_form.html"
    success_url = reverse_lazy("event_list")


class EventDeleteView(DeleteView):
    model = SchoolEvent
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("event_list")






# # =============================================
# # SCHOOL EVENTS
# # =============================================
# class EventListView(LoginRequiredMixin, ListView):
#     model = SchoolEvent
#     template_name = "superuser/event_list.html"
#     context_object_name = "events"
#     ordering = ['-start_date']


# class EventDetailView(LoginRequiredMixin, DetailView):
#     model = SchoolEvent
#     template_name = "superuser/event_detail.html"
#     context_object_name = "event"


# class EventCreateView(LoginRequiredMixin, CreateView):
#     model = SchoolEvent
#     form_class = SchoolEventForm
#     template_name = "superuser/event_form.html"
#     success_url = reverse_lazy("event_list")

#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_superuser:
#             return render(request, "400.html")
#         return super().dispatch(request, *args, **kwargs)


# class EventUpdateView(LoginRequiredMixin, UpdateView):
#     model = SchoolEvent
#     form_class = SchoolEventForm
#     template_name = "superuser/event_form.html"
#     success_url = reverse_lazy("event_list")


# class EventDeleteView(LoginRequiredMixin, DeleteView):
#     model = SchoolEvent
#     template_name = "superuser/event_confirm_delete.html"
#     success_url = reverse_lazy("event_list")


# # =============================================
# # EVENT GALLERY / DOCUMENT UPLOAD
# # =============================================
# class EventGalleryUploadView(LoginRequiredMixin, CreateView):
#     model = EventGallery
#     form_class = EventGalleryForm
#     template_name = "superuser/event_gallery_form.html"

#     def form_valid(self, form):
#         event = SchoolEvent.objects.get(pk=self.kwargs['pk'])
#         form.instance.event = event
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy("event_detail", kwargs={'pk': self.kwargs['pk']})


# class EventDocumentUploadView(LoginRequiredMixin, CreateView):
#     model = EventDocument
#     form_class = EventDocumentForm
#     template_name = "superuser/event_document_form.html"

#     def form_valid(self, form):
#         event = SchoolEvent.objects.get(pk=self.kwargs['pk'])
#         form.instance.event = event
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy("event_detail", kwargs={'pk': self.kwargs['pk']})