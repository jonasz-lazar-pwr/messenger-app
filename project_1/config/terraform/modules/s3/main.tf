# s3/main.tf

# === GŁÓWNY ZASÓB ===

resource "aws_s3_bucket" "this" {
  bucket        = var.bucket_name
  force_destroy = true                   # Pozwala na usunięcie bucketa razem z zawartością
  tags          = var.tags
}

# === ZABEZPIECZENIA I DOSTĘP ===

resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id

  block_public_acls       = true         # Blokuje stosowanie publicznych ACL
  ignore_public_acls      = true         # Ignoruje istniejące publiczne ACL
  block_public_policy     = false        # Pozwala na publiczne polityki (np. do publicznego GET)
  restrict_public_buckets = false        # Pozwala na dostęp publiczny do obiektów
}

resource "aws_s3_bucket_policy" "this" {
  bucket = aws_s3_bucket.this.id

  policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = "*",
        Action    = [
          "s3:PutBucketPolicy",
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.this.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.this.bucket}/*"
        ]
      }
    ]
  })
}

# === WŁASNOŚĆ I UPRAWNIENIA ===

resource "aws_s3_bucket_ownership_controls" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    object_ownership = "BucketOwnerEnforced"    # Wymusza przypisanie plików do właściciela bucketa
  }
}

# === WERSJONOWANIE ===

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id

  versioning_configuration {
    status = "Suspended"    # Wersjonowanie wyłączone
  }
}

# === SZYFROWANIE ===

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"           # Domyślne szyfrowanie typu SSE-S3
    }
  }
}
