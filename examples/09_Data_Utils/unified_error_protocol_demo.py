import pandas as pd
import paperplot as pp


def main():
    df = pd.DataFrame(
        {
            "time": [0, 1, 2, 3],
            "signal": [1.0, 1.2, 1.4, 1.3],
            "signal_err": [0.05, 0.08, 0.06, 0.07],
        }
    )

    (
        pp.Plotter(layout=(1, 1), style="publication")
        .add_line(data=df, x="time", y="signal", err="signal_err", capsize=3, label="signal")
        .set_title("Unified line error protocol")
        .set_xlabel("Time")
        .set_ylabel("Signal")
        .set_legend()
        .save("unified_error_protocol_demo.png")
    )


if __name__ == "__main__":
    main()
