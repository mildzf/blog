from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin


class AuthorListView(ListView):
    """ Sub-class of the ListView"""


class AuthorDetailView(DetailView):
    """Sub-class of the DetailView""" 


class AuthorCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-class of the CreateView to automatically to 
    add the author to the saved object.
    """

    # Saves the form instance, sets the current object for the view, and redirects to get_success_url().
    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.save()
        return super(AuthorCreateView, self).form_valid(form)



class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.
    """

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        qs = super(AuthorUpdateView, self).get_queryset()
        return qs.filter(author=self.request.user)


class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """

    def get_queryset(self):
        qs = super(AuthorDeleteView, self).get_queryset()
        return qs.filter(author=self.request.user)