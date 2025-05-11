import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { ChatService } from '../../../../services/chat.service';

@Component({
  selector: 'app-chat-list',
  standalone: false,
  templateUrl: './chat-list.component.html',
  styleUrl: './chat-list.component.css'
})
export class ChatListComponent implements OnInit {
  chats: any[] = [];
  selectedChat: any = null;

  @Output() chatSelected = new EventEmitter<any>();
  @Output() chatCreated = new EventEmitter<any>();
  @Output() logout = new EventEmitter<void>();

  constructor(private chatService: ChatService) {}

  ngOnInit(): void {
    this.loadChats();
  }

  loadChats(): void {
    this.chatService.getChats().subscribe(data => {
      this.chats = data;
    });
  }

  onSelect(chat: any): void {
    this.selectedChat = chat;
    this.chatSelected.emit(chat);
  }

  onChatCreated(newChat: any): void {
    this.chatCreated.emit(newChat);
    this.loadChats(); // Refresh list
    this.selectedChat = newChat;
    this.chatSelected.emit(newChat);
  }

  onLogout(): void {
    this.logout.emit();
  }
}

// import { Component, Input, Output, EventEmitter } from '@angular/core';
//
// @Component({
//   selector: 'app-chat-list',
//   standalone: false,
//   templateUrl: './chat-list.component.html',
//   styleUrl: './chat-list.component.css'
// })
// export class ChatListComponent {
//   // List of chats to display
//   @Input() chats: any[] = [];
//   // Currently selected chat
//   @Input() selectedChat: any = null;
//   // Event emitted when a chat is selected
//   @Output() chatSelected = new EventEmitter<any>();
//   // Event emitted when the user clicks the logout button
//   @Output() logout = new EventEmitter<void>();
//
//   // Triggered on chat click
//   onSelect(chat: any): void {
//     this.chatSelected.emit(chat);
//   }
// }
