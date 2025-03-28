# Large File Uploader with S3 Signed URLs

![React](https://img.shields.io/badge/react-%2320232a.svg?style=flat-square&logo=react&logoColor=%2361DAFB)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=flat-square&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=flat-square&logo=vite&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat-square&logo=amazon-aws&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon%20S3-FF9900?style=flat-square&logo=amazons3&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=flat-square&logo=docker&logoColor=white)

![large-file-uploader](https://socialify.git.ci/nicholasadamou/s3-large-file-uploader/image?language=1&forks=1&issues=1&name=1&owner=1&pattern=Circuit+Board&pulls=1&stargazers=1&theme=Dark)

This project demonstrates how to upload large files (20GB+) directly to Amazon S3 using signed URLs — with a Python + FastAPI backend, MongoDB for tracking, and a React + Vite frontend.

📖 Read the full article on my blog: [How to Upload Large Files (20GB+) to S3 using Signed URLs](https://nicholasadamou.com/notes/handling-large-file-uploads-20gb-in-fast-api-with-s3-multipart-upload-using-signed-urls)

> This repo focuses on showcasing the complete flow — from multipart upload creation to chunk uploads, progress tracking, and final completion.

Feel free to explore, fork, and adapt it to your use case!

## Project Architecture

### Why a Monorepo?

This project is structured as a monorepo for several key reasons:

1. **Unified Development Experience**: The frontend and backend components are tightly coupled in their functionality. A monorepo allows for easier coordination between these components during development.

2. **Simplified Dependency Management**: Shared configurations and dependencies can be managed more efficiently, reducing duplication and ensuring consistency.

3. **Atomic Changes**: Changes that span both frontend and backend can be committed together, ensuring the system remains in a consistent state.

4. **Streamlined CI/CD**: Deployment pipelines can be configured to understand the relationships between components, allowing for more intelligent build and deployment processes.

### Technology Choices

#### Frontend (React + TypeScript + Vite)

- **React**: Provides a component-based architecture ideal for building the interactive UI elements needed for file upload tracking.
- **TypeScript**: Adds type safety to prevent common errors and improve developer experience.
- **Vite**: Offers lightning-fast HMR (Hot Module Replacement) and optimized builds, significantly improving development speed.

#### Backend (Python + FastAPI)

- **FastAPI**: Chosen for its high performance, automatic API documentation, and built-in validation through Pydantic.
- **Async Support**: Efficiently handles concurrent S3 operations, crucial for multipart uploads.
- **Type Hints**: Provides automatic validation and editor support, reducing bugs.

#### Database (MongoDB)

- **Document Model**: Perfect match for the variable metadata of upload sessions.
- **Flexible Schema**: Adapts to changing requirements without migrations.
- **Performance**: Document-level concurrency supports high-throughput operations for tracking many simultaneous uploads.

#### Cloud Storage (AWS S3)

- **Scalability**: Handles files of any size with consistent performance.
- **Multipart Upload API**: Native support for chunked uploads of large files.
- **Direct Upload**: Signed URLs allow clients to upload directly to S3, reducing server load.

## How It Works

The large file upload process follows these steps:

1. **Initialization**: Frontend requests a multipart upload from the backend
2. **Chunking**: File is split into manageable chunks (typically 5-10MB each)
3. **Parallel Uploads**: Chunks are uploaded directly to S3 using pre-signed URLs
4. **Progress Tracking**: Backend tracks upload progress in MongoDB
5. **Completion**: Once all chunks are uploaded, backend completes the multipart upload

This approach offers several advantages:
- Bypasses API Gateway and server upload limits
- Reduces server load by having clients upload directly to S3
- Provides resilience through resumable uploads
- Enables real-time progress tracking

## Getting Started

See the README files in the [`frontend/`](frontend/) and [`backend/`](backend/) directories for specific setup instructions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
