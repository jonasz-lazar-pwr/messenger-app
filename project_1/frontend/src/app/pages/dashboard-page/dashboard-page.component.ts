import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { ConversationService } from '../../services/conversation.service';
import { MessageService } from '../../services/message.service';
import { interval, Subscription } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-dashboard-page',
  standalone: false,
  templateUrl: './dashboard-page.component.html',
  styleUrls: ['./dashboard-page.component.css']
})
export class DashboardPageComponent implements OnInit, OnDestroy {
  // UI + app state
  conversations: any[] = [];
  selectedConversation: any = null;
  messages: any[] = [];
  newMessage: string = '';
  selectedFile: File | null = null;

  // Auth state
  userSub: string | null = null;

  // Polling
  messagePollingSub: Subscription | null = null;

  // Reference to scroll target element
  @ViewChild('messagesEnd') messagesEnd!: ElementRef;

  constructor(
    private conversationService: ConversationService,
    private messageService: MessageService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    // Get current user sub from token
    this.userSub = this.authService.getUserSub();

    // Load conversation list on init
    this.conversationService.getConversations().subscribe(data => {
      this.conversations = data;
    });
  }

  ngOnDestroy(): void {
    // Clean up polling on destroy
    this.messagePollingSub?.unsubscribe();
  }

  selectConversation(conversation: any): void {
    this.selectedConversation = conversation;
    this.messages = [];

    // Load initial messages
    this.messageService.getMessages(conversation.id).subscribe((msgs) => {
      this.messages = msgs;
      this.scrollToBottom();
    });

    // Clear previous polling (if any)
    this.messagePollingSub?.unsubscribe();

    // Poll for new messages every 10 seconds
    this.messagePollingSub = interval(10000).pipe(
      switchMap(() => this.messageService.getMessages(conversation.id))
    ).subscribe((msgs) => {
      this.messages = msgs;
      this.scrollToBottom();
    });
  }

  handleFileSelect(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
    }
  }

  handleSend(): void {
    if (!this.selectedConversation) return;

    if (this.selectedFile) {
      // Send media message (file)
      this.messageService.sendMediaMessage(this.selectedConversation.id, this.selectedFile).subscribe((msg) => {
        this.messages.push(msg);
        this.selectedFile = null;
        this.scrollToBottom();
      });
    } else if (this.newMessage.trim()) {
      // Send text message
      this.messageService.sendTextMessage(this.selectedConversation.id, this.newMessage).subscribe((msg) => {
        this.messages.push(msg);
        this.newMessage = '';
        this.scrollToBottom();
      });
    }
  }

  scrollToBottom(): void {
    // Scroll to last message (for better UX)
    setTimeout(() => {
      this.messagesEnd?.nativeElement?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  }

  clearSelectedFile(): void {
    // Cancel attached media file
    this.selectedFile = null;
  }

  logout(): void {
    this.authService.logout();
  }
}
