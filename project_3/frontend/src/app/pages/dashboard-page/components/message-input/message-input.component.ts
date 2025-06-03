import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MessageService } from '../../../../services/message.service';


@Component({
  selector: 'app-message-input',
  standalone: false,
  templateUrl: './message-input.component.html',
  styleUrl: './message-input.component.css'
})
export class MessageInputComponent {
  @Input() chatId!: number;
  @Output() messageSent = new EventEmitter<any>();

  newMessage: string = '';
  selectedFile: File | null = null;
  sending: boolean = false;

  constructor(
    private messageService: MessageService
  ) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) this.selectedFile = file;
  }

  clearSelectedFile(): void {
    this.selectedFile = null;
  }

  send(): void {
    if (!this.chatId || this.sending) return;

    this.sending = true;

    if (this.selectedFile) {
      this.messageService.sendMediaMessage(this.chatId, this.selectedFile).subscribe({
        next: (msg) => {
          this.selectedFile = null;
          this.messageSent.emit();
          this.sending = false;
        },
        error: () => {
          this.sending = false;
        }
      });
    } else if (this.newMessage.trim()) {
      this.messageService.sendTextMessage(this.chatId, this.newMessage).subscribe({
        next: (msg) => {
          this.newMessage = '';
          this.messageSent.emit();
          this.sending = false;
        },
        error: () => {
          this.sending = false;
        }
      });
    } else {
      this.sending = false;
    }
  }
}
