from easydict import EasyDict

collector_env_num = 3
evaluator_env_num = 2
trading_position_r2d2_config = dict(
    exp_name='trading_position_r2d2_seed0',
    env=dict(
        collector_env_num=collector_env_num,
        evaluator_env_num=evaluator_env_num,
        n_evaluator_episode=evaluator_env_num,

        positions=[-2, -1, 0, 1, 2],
        # Prev number of kline will keep obs and LSTM NN will use it for choose the action of next step
        windows=20,
        trading_fees=0.0001,
        borrow_interest_rate=0.0003/100,
        portfolio_initial_value=1000,
        initial_position='random',
        start_date='2018-01-01',
        end_date='2023-08-10',
        train_range=0.7,
        test_range=0.3,
        trading_currency='BTCUSDT',
        indicators=['close_9_ema', 'rsi_14'],
        is_train=True,
        is_render=False,
        verbose=1,
        env_id="trading_position",
        render_mode="logs",
        df=None,
        manager=dict(
            shared_memory=False,
            episode_num=float('inf'),
            max_retry=5,
            step_timeout=None,
            auto_reset=True,
            reset_timeout=None,
            retry_type='reset',
            retry_waiting_time=0.1,
            copy_on_get=True,
            context='fork',
            wait_num=float('inf'),
            step_wait_timeout=None,
            connect_timeout=60,
            reset_inplace=False,
            cfg_type='SyncSubprocessEnvManagerDict',
            type='subprocess',
        )
    ),
    policy=dict(
        cuda=True,
        priority=True,
        priority_IS_weight=False,
        discount_factor=0.9,
        nstep=10,
        burnin_step=2,
        learn_unroll_len=20,
        model=dict(
            # window_size x obs features = 20 x 9 = 180 (This shape is used for RNN and input shape of Conv2d).
            obs_shape=140,
            action_shape=5,
            # Used for output of Linear layer.
            encoder_hidden_size_list=[512, 512, 512]
        ),
        learn=dict(
            update_per_collect=3,
            batch_size=64,
            learning_rate=0.00001,
            target_update_freq=500,
            iqn=True,
        ),
        collect=dict(
            n_sample=64,
            unroll_len= 2 + 20,
            env_num=collector_env_num,
        ),
        eval=dict(env_num=evaluator_env_num, evaluator=dict(eval_freq=1440, )),
        other=dict(
            eps=dict(
                type='exp',
                start=0.95,
                end=0.1,
                decay=10000,
            ), replay_buffer=dict(replay_buffer_size=100000, )
        ),
    ),
)
trading_position_r2d2_config = EasyDict(trading_position_r2d2_config)
main_config = trading_position_r2d2_config
trading_position_r2d2_create_config = dict(
    env=dict(
        type='trading_position',
        import_names=['envs.trading_position.trading_position_env'],
    ),
    env_manager=dict(type='subprocess'),
    policy=dict(type='r2d2'),
)
trading_position_r2d2_create_config = EasyDict(trading_position_r2d2_create_config)
create_config = trading_position_r2d2_create_config

if __name__ == "__main__":
    # or you can enter `ding -m serial -c trading_position_r2d2_config.py -s 0`
    from ding.entry import serial_pipeline

    serial_pipeline((main_config, create_config), seed=0)
