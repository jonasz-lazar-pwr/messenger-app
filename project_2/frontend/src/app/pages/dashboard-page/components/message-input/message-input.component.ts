import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MessageService } from '../../../../services/message.service';
import { MessageStoreService } from '../../../../services/message-store.service';

@Component({
  selector: 'app-message-input',
  standalone: false,
  templateUrl: './message-input.component.html',
  styleUrl: './message-input.component.css'
})
export class MessageInputComponent {
  @Input() chatId!: number;
  @Output() messageSent = new EventEmitter<void>();

  newMessage: string = '';
  selectedFile: File | null = null;

  constructor(
    private messageService: MessageService,
    private messageStore: MessageStoreService
  ) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) this.selectedFile = file;
  }

  clearSelectedFile(): void {
    this.selectedFile = null;
  }

  send(): void {
    if (!this.chatId) return;

    if (this.selectedFile) {
      this.messageService.sendMediaMessage(this.chatId, this.selectedFile).subscribe(msg => {
        this.messageStore.setMessages([...this.messageStore.getMessages(), msg]);
        this.selectedFile = null;
        this.messageSent.emit();
      });
    } else if (this.newMessage.trim()) {
      this.messageService.sendTextMessage(this.chatId, this.newMessage).subscribe(msg => {
        this.messageStore.setMessages([...this.messageStore.getMessages(), msg]);
        this.newMessage = '';
        this.messageSent.emit();
      });
    }
  }
}
