import graphene
from graphene_django import DjangoObjectType

from api.models import Users, Event


class UserType(DjangoObjectType):
    class Meta:
        model = Users
        fields = ('id', 'username', 'password', 'email')


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = '__all__'


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, user_data=None):
        user = Users.objects.create_user(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email
        )
        return CreateUser(user=user)


EventChoice = EventType._meta.fields["reminder"].type


class EventUserInput(graphene.InputObjectType):
    username = graphene.String()


class EventInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    text = graphene.String(required=True)
    date = graphene.DateTime(required=True)
    reminder = graphene.List(of_type=EventChoice)
    creator = graphene.String()


class CreateEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    def mutate(root, info, event_data=None):
        user = Users.objects.get(username=event_data.creator)
        event = Event.objects.create(
            title=event_data.title,
            text=event_data.text,
            date=event_data.date,
            reminder=event_data.reminder[0],
            creator=user
        )
        return CreateEvent(event=event)


class MyMutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_event = CreateEvent.Field()


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    users = graphene.List(UserType)
    events = graphene.List(EventType)

    def resolve_users(root, info):
        return Users.objects.all()

    def resolve_events(root, info):
        return Event.objects.all()


schema = graphene.Schema(query=Query, mutation=MyMutations)
