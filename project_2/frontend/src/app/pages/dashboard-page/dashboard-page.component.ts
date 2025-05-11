import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { ChatService } from '../../services/chat.service';
import { MessageService } from '../../services/message.service';
import { MessageStoreService } from '../../services/message-store.service';
import { MediaLoaderService } from '../../services/media-loader.service';
import { interval, Subscription } from 'rxjs';
import { switchMap } from 'rxjs/operators';

type ViewMode = 'chats' | 'users';

@Component({
  selector: 'app-dashboard-page',
  standalone: false,
  templateUrl: './dashboard-page.component.html',
  styleUrls: ['./dashboard-page.component.css']
})
export class DashboardPageComponent implements OnInit, OnDestroy {
  // Currently selected chat
  selectedChat: any = null;

  // User subscription ID
  userSub: string | null = null;

  // Flag indicating if messages are being loaded
  loadingMessages: boolean = false;

  // Subscription for message polling
  messagePollingSub: Subscription | null = null;

  activeView: ViewMode = 'chats';

  @ViewChild('chatWindow') chatWindowRef!: any;

  constructor(
    private authService: AuthService,
    private messageService: MessageService,
    private messageStore: MessageStoreService,
    private mediaLoader: MediaLoaderService
  ) {}

  ngOnInit(): void {
    this.userSub = this.authService.getUserSub();
  }

  // Called when component is destroyed
  ngOnDestroy(): void {
    this.messagePollingSub?.unsubscribe();
  }

  switchView(view: 'chats' | 'users') {
    this.activeView = view;
    this.selectedChat = null;
  }

  // Called when a chat is selected from the sidebar
  selectChat(chat: any): void {
    this.selectedChat = chat;
    this.loadingMessages = true;
    this.messageStore.setMessages([]);

    this.messageService.getMessages(chat.id).subscribe(async (initial) => {
      const prepared = initial.map(msg => ({
        ...msg,
        loadFailed: false,
        loading: !!msg.media_url
      }));

      // Preload all images before rendering the messages
      await Promise.allSettled(
        prepared.map(msg =>
          msg.media_url ? this.mediaLoader.preloadImage(msg) : Promise.resolve()
        )
      );

      this.messageStore.setMessages(prepared);
      this.loadingMessages = false;
      this.chatWindowRef?.scrollToBottom?.();
    });

    this.messagePollingSub?.unsubscribe();
    this.messagePollingSub = interval(10000)
      .pipe(switchMap(() => this.messageService.getMessages(chat.id)))
      .subscribe((newMsgs) => {
        if (this.messageStore.isNewMessageList(newMsgs)) {
          this.messageStore.updateMessagesPreservingState(newMsgs);
          this.chatWindowRef?.scrollToBottom?.();
        }
      });
  }

  onMessageSent(): void {
    this.chatWindowRef?.scrollToBottom();
  }

  onChatCreated(chat: any): void {
    this.switchView('chats');
    this.selectChat(chat);
  }

  // Logs out the current user
  logout(): void {
    this.authService.logout();
  }

  // Getter for current list of messages (from message store)
  get messages(): any[] {
    return this.messageStore.getMessages();
  }
}
