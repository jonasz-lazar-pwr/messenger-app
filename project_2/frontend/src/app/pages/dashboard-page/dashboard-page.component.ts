import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { MessageService } from '../../services/message.service';
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
  selectedChat: any = null;
  userSub: string | null = null;
  messages: any[] = [];
  loadingMessages: boolean = false;
  messagePollingSub: Subscription | null = null;
  activeView: ViewMode = 'chats';

  @ViewChild('chatWindow') chatWindowRef!: any;

  constructor(
    private authService: AuthService,
    private messageService: MessageService,
    private mediaLoader: MediaLoaderService
  ) {}

  ngOnInit(): void {
    this.userSub = this.authService.getUserSub();
  }

  // Called when component is destroyed
  ngOnDestroy(): void {
    this.stopPolling();
  }

  switchView(view: ViewMode): void {
    this.activeView = view;
    this.selectedChat = null;
    this.messages = [];
    this.stopPolling();
  }

  // Called when a chat is selected from the sidebar
  selectChat(chat: any): void {
    this.selectedChat = chat;
    this.messages = [];
    this.loadingMessages = true;

    this.loadMessagesOnce();

    this.stopPolling();
    this.messagePollingSub = interval(10000)
      .pipe(switchMap(() => this.messageService.getMessages(chat.id)))
      .subscribe(messages => this.updateMessages(messages));
  }

  stopPolling(): void {
    this.messagePollingSub?.unsubscribe();
    this.messagePollingSub = null;
  }


  loadMessagesOnce(): void {
    this.messageService.getMessages(this.selectedChat.id).subscribe(async (msgs) => {
      const prepared = msgs.map(msg => ({
        ...msg,
        loadFailed: false,
        loading: !!msg.media_url
      }));

      await Promise.allSettled(
        prepared.map(msg =>
          msg.media_url ? this.mediaLoader.preloadImage(msg) : Promise.resolve()
        )
      );

      this.messages = prepared;
      this.loadingMessages = false;
      this.chatWindowRef?.scrollToBottom?.();
    });
  }

  updateMessages(newMsgs: any[]): void {
    this.messages = newMsgs.map(msg => ({
      ...msg,
      loadFailed: false,
      loading: !!msg.media_url
    }));
    this.chatWindowRef?.scrollToBottom?.();
  }

  onMessageSent(): void {
    this.loadMessagesOnce();
  }

  onChatCreated(chat: any): void {
    this.switchView('chats');
    this.selectChat(chat);
  }

  // Logs out the current user
  logout(): void {
    this.authService.logout();
  }
}
