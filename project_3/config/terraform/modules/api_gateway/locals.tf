# api_gateway/locals.tf

# Lista wszystkich endpointów HTTP wraz z metodą, ścieżką i informacją, czy wymagają autoryzacji Cognito
locals {
  routes = {
    health_check = {
      method     = "GET"
      path       = "/api/health"
      authorizer = false
    }
    health_check_secure = {
      method     = "GET"
      path       = "/api/health/secure"
      authorizer = true
    }
    register_user = {
      method     = "POST"
      path       = "/api/users/register"
      authorizer = true
    }
    get_chats = {
      method     = "GET"
      path       = "/api/chats"
      authorizer = true
    }
    search_users = {
      method     = "GET"
      path       = "/api/users/search"
      authorizer = true
    }
    create_chat = {
      method     = "POST"
      path       = "/api/chats"
      authorizer = true
    }
    get_messages = {
      method     = "GET"
      path       = "/api/messages/{chat_id}"
      authorizer = true
    }
    send_message_text = {
      method     = "POST"
      path       = "/api/messages/text"
      authorizer = true
    }
    send_message_media = {
      method     = "POST"
      path       = "/api/messages/media"
      authorizer = true
    }
  }
}
