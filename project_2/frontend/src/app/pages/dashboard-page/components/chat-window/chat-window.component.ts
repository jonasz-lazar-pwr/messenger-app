import { Component, ElementRef, Input, ViewChild, AfterViewChecked, ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-chat-window',
  standalone: false,
  templateUrl: './chat-window.component.html',
  styleUrls: ['./chat-window.component.css']
})
export class ChatWindowComponent implements AfterViewChecked {
  @Input() selectedChat: any;
  @Input() userSub: string | null = null;
  @Input() messages: any[] = [];
  @Input() loadingMessages: boolean = false;

  @ViewChild('messagesEnd') messagesEnd!: ElementRef;

  constructor(
    private cdRef: ChangeDetectorRef
  ) {}

  ngAfterViewChecked(): void {
    // Ensure DOM is fully updated before scrolling
    this.scrollToBottom();
  }

  handleMediaLoadError(message: any): void {
    message.loadFailed = true;
    message.loading = false;
  }

  handleMediaLoaded(message: any): void {
    message.loading = false;
  }

  scrollToBottom(): void {
    setTimeout(() => {
      try {
        this.messagesEnd?.nativeElement?.scrollIntoView({ behavior: 'smooth' });
      } catch (_) {}
    }, 100);
  }
}
