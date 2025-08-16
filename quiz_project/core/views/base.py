from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class BaseListView(ListView):    paginate_by = 20
class BaseDetailView(DetailView): pass
class BaseCreateView(CreateView): success_url = None
class BaseUpdateView(UpdateView): success_url = None
class BaseDeleteView(DeleteView): success_url = None

def success_url_to(name: str):
    """Factory para success_url perezoso."""
    return reverse_lazy(name)
