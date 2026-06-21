import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ResumeService, ResumeResponse } from '../../services/resume.service';

@Component({
    selector: 'app-upload',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './upload.component.html',
    styleUrls: ['./upload.component.css']
})
export class UploadComponent {
    selectedFile: File | null = null;
    uploading = false;
    uploadResult: ResumeResponse | null = null;
    error: string | null = null;
    dragOver = false;

    constructor(private resumeService: ResumeService) { }

    onDragOver(event: DragEvent) {
        event.preventDefault();
        event.stopPropagation();
        this.dragOver = true;
    }

    onDragLeave(event: DragEvent) {
        event.preventDefault();
        event.stopPropagation();
        this.dragOver = false;
    }

    onDrop(event: DragEvent) {
        event.preventDefault();
        event.stopPropagation();
        this.dragOver = false;

        const files = event.dataTransfer?.files;
        if (files && files.length > 0) {
            this.handleFile(files[0]);
        }
    }

    onFileSelected(event: Event) {
        const input = event.target as HTMLInputElement;
        if (input.files && input.files.length > 0) {
            this.handleFile(input.files[0]);
        }
    }

    handleFile(file: File) {
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword', 'text/plain'];

        if (!allowedTypes.includes(file.type)) {
            this.error = 'Invalid file type. Please upload PDF, DOCX, or TXT files only.';
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            this.error = 'File size exceeds 10MB limit.';
            return;
        }

        this.selectedFile = file;
        this.error = null;
        this.uploadResult = null;
    }

    uploadResume() {
        if (!this.selectedFile) {
            this.error = 'Please select a file first.';
            return;
        }

        this.uploading = true;
        this.error = null;
        this.uploadResult = null;

        this.resumeService.uploadResume(this.selectedFile).subscribe({
            next: (response) => {
                this.uploading = false;
                this.uploadResult = response;
                this.selectedFile = null;
            },
            error: (err) => {
                this.uploading = false;
                this.error = err.error?.detail || 'Failed to upload resume. Please try again.';
            }
        });
    }

    clearFile() {
        this.selectedFile = null;
        this.uploadResult = null;
        this.error = null;
    }
}
