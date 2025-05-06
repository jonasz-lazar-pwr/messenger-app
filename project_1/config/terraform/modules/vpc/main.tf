# vpc/main.tf

resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = var.vpc_name
  }
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "${var.vpc_name}-igw"
  }
}

resource "aws_subnet" "frontend" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.subnet_cidrs["frontend"]
  availability_zone       = var.availability_zones["frontend"]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-frontend-subnet"
  }
}

resource "aws_subnet" "frontend_alt" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.subnet_cidrs["frontend_alt"]
  availability_zone       = var.availability_zones["frontend_alt"]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-frontend-alt-subnet"
  }
}

resource "aws_subnet" "backend" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.subnet_cidrs["backend"]
  availability_zone       = var.availability_zones["backend"]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-backend-subnet"
  }
}

resource "aws_subnet" "backend_alt" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.subnet_cidrs["backend_alt"]
  availability_zone       = var.availability_zones["backend_alt"]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-backend-alt-subnet"
  }
}

resource "aws_subnet" "database" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.subnet_cidrs["database"]
  availability_zone       = var.availability_zones["database"]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-database-subnet"
  }
}

resource "aws_subnet" "database_alt" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.subnet_cidrs["database_alt"]
  availability_zone       = var.availability_zones["database_alt"]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-database-alt-subnet"
  }
}

# --- Routing ---
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "${var.vpc_name}-public-rt"
  }
}

resource "aws_route" "default_route" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.this.id
}

resource "aws_route_table_association" "frontend" {
  subnet_id      = aws_subnet.frontend.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "frontend_alt" {
  subnet_id      = aws_subnet.frontend_alt.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "backend" {
  subnet_id      = aws_subnet.backend.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "backend_alt" {
  subnet_id      = aws_subnet.backend_alt.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "database" {
  subnet_id      = aws_subnet.database.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "database_alt" {
  subnet_id      = aws_subnet.database_alt.id
  route_table_id = aws_route_table.public.id
}

# --- Security Groups ---

resource "aws_security_group" "frontend" {
  name        = "${var.vpc_name}-frontend-sg"
  description = "Controls traffic TO frontend instances (HTTP/HTTPS)"
  vpc_id      = aws_vpc.this.id

  ingress {
    description = "Allow HTTP from anywhere (for ALB or browser)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "${var.vpc_name}-frontend-sg"
  }
}

resource "aws_security_group" "backend" {
  name        = "${var.vpc_name}-backend-sg"
  description = "Controls traffic TO backend instances (HTTP/HTTPS)"
  vpc_id      = aws_vpc.this.id

  ingress {
    description = "Allow HTTP from anywhere (for ALB)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow HTTPS from anywhere (for ALB)"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.vpc_name}-backend-sg"
  }
}

resource "aws_security_group" "database" {
  name        = "${var.vpc_name}-database-sg"
  description = "Allow PostgreSQL from anywhere (testing only!)"
  vpc_id      = aws_vpc.this.id

  ingress {
    description = "Allow PostgreSQL from anywhere (NOT SAFE FOR PRODUCTION)"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.vpc_name}-database-sg"
  }
}