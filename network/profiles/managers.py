from django.db.models import Manager, Q

from profiles.models import Profile, Relationship


class ProfileManager(Manager):
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(
            Q(sender=profile)
            | Q(receiver=profile)
        )

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        avaliable = [profile for profile in profiles if profile not in accepted]
        return avaliable

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class RelationshipManager(Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs
