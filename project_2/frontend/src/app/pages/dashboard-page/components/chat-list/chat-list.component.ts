import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { ChatService } from '../../../../services/chat.service';


@Component({
  selector: 'app-chat-list',
  standalone: false,
  templateUrl: './chat-list.component.html',
  styleUrl: './chat-list.component.css'
})
export class ChatListComponent implements OnInit {
  chats: any[] = [];
  loadingChats: boolean = true;

  @Input() selectedChat: any;

  @Output() chatSelected = new EventEmitter<any>();
  @Output() chatCreated = new EventEmitter<any>();
  @Output() logout = new EventEmitter<void>();

  constructor(private chatService: ChatService) {}

  ngOnInit(): void {
    this.loadChats();
  }

  loadChats(): void {
    this.loadingChats = true;
    this.chatService.getChats().subscribe({
      next: (data) => {
        this.chats = data;
        this.loadingChats = false;
      },
      error: (_) => {
        this.loadingChats = false;
      }
    });
  }

  onSelect(chat: any): void {
    this.selectedChat = chat;
    this.chatSelected.emit(chat);
  }
}
