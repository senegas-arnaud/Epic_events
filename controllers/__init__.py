from controllers.auth import create_admin, login, logout, get_current_user
from controllers.collaborator import create_collaborator, update_collaborator, delete_collaborator, get_all_collaborators
from controllers.client import create_client, update_client, get_all_clients, get_my_clients
from controllers.contract import create_contract, update_contract, get_all_contracts, get_unsigned_contracts, get_unpaid_contracts, get_my_contracts
from controllers.event import create_event, assign_support, update_event, get_all_events, get_my_events, get_events_without_support