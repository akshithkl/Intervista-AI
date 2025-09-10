
// frontend/src/components/InterviewPractice.jsx
import React, { useState } from "react";
import {
  Box,
  Button,
  TextField,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  Chip,
  IconButton
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack"; // ✅ Correct import
import { aiAPI } from "../services/api";

const InterviewPractice = ({ selectedJob }) => {
  const [question, setQuestion] = useState("");
  const [userAnswer, setUserAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateQuestion = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await aiAPI.generateQuestion({
        job_role: selectedJob?.title || "Software Engineer",
        experience_level: "beginner",
      });
      setQuestion(response.data.question);
      setUserAnswer("");
      setFeedback("");
    } catch (err) {
      setError("Failed to generate question. Try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const evaluateAnswer = async () => {
    if (!userAnswer.trim()) return;
    setLoading(true);
    setError("");
    try {
      const response = await aiAPI.evaluateAnswer({
        question,
        answer: userAnswer,
        job_role: selectedJob?.title || "Software Engineer",
      });
      setFeedback(response.data.feedback);
    } catch (err) {
      setError("Failed to evaluate answer. Try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const resetSession = () => {
    setQuestion("");
    setUserAnswer("");
    setFeedback("");
    setError("");
  };

  return (
    <Box sx={{ maxWidth: 800, margin: "0 auto", padding: 3 }}>
      <Box sx={{ display: "flex", alignItems: "center", mb: 3 }}>
        <IconButton onClick={resetSession} sx={{ mr: 2 }}>
          <ArrowBackIcon />
        </IconButton>
        <Typography variant="h4">🎯 Interview Practice</Typography>
      </Box>

      {selectedJob && (
        <Chip label={`Practicing: ${selectedJob.title}`} color="primary" sx={{ mb: 3 }} />
      )}

      {!question ? (
        <Box sx={{ textAlign: "center", py: 4 }}>
          <Button
            variant="contained"
            size="large"
            onClick={generateQuestion}
            disabled={loading}
          >
            {loading ? <CircularProgress size={20} /> : "Start Practice Session"}
          </Button>
        </Box>
      ) : (
        <>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" color="primary">
                💡 Question:
              </Typography>
              <Typography sx={{ fontStyle: "italic", fontSize: "1.1rem" }}>
                "{question}"
              </Typography>
            </CardContent>
          </Card>

          <TextField
            fullWidth
            multiline
            rows={6}
            label="Your Answer"
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
            placeholder="Type your answer here..."
            sx={{ mb: 2 }}
            disabled={loading}
          />

          <Box sx={{ display: "flex", gap: 2, mb: 3 }}>
            <Button variant="outlined" onClick={generateQuestion} disabled={loading}>
              New Question
            </Button>
            <Button
              variant="contained"
              onClick={evaluateAnswer}
              disabled={loading || !userAnswer.trim()}
              startIcon={loading ? <CircularProgress size={20} /> : null}
            >
              {loading ? "Evaluating..." : "Get Feedback"}
            </Button>
          </Box>
        </>
      )}

      {error && <Alert severity="error">{error}</Alert>}
      {feedback && (
        <Card sx={{ bgcolor: "info.light" }}>
          <CardContent>
            <Typography variant="h6">📝 AI Feedback:</Typography>
            <Typography sx={{ whiteSpace: "pre-wrap" }}>{feedback}</Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default InterviewPractice;

