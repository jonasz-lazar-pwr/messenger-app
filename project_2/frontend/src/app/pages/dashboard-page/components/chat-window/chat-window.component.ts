import {
  Component,
  ElementRef,
  Input,
  ViewChild,
  AfterViewChecked,
  OnChanges
} from '@angular/core';


@Component({
  selector: 'app-chat-window',
  standalone: false,
  templateUrl: './chat-window.component.html',
  styleUrls: ['./chat-window.component.css']
})
export class ChatWindowComponent implements AfterViewChecked, OnChanges {
  @Input() selectedChat: any;
  @Input() userSub: string | null = null;
  @Input() messages: any[] = [];
  @Input() loadingMessages: boolean = false;

  @ViewChild('messagesEnd') messagesEnd!: ElementRef;

  private autoScrollEnabled = true;

  ngAfterViewChecked(): void {
    if (this.autoScrollEnabled) {
      this.scrollToBottom();
      this.autoScrollEnabled = false;
    }
  }

  ngOnChanges(): void {
    this.autoScrollEnabled = true;
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
